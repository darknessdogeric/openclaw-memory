#!/usr/bin/env python3
"""
Captcha Solver - 验证码自动处理模块
支持滑块验证码、点选验证码等
"""

import asyncio
import base64
import json
import time
from typing import Optional, Tuple, Dict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CaptchaResult:
    """验证码识别结果"""
    success: bool
    solution: Optional[Dict]
    cost_time: float
    error_message: Optional[str] = None


class CaptchaSolver:
    """验证码解决器基类"""
    
    def __init__(self):
        pass
    
    async def solve(self, captcha_image: bytes, captcha_type: str) -> CaptchaResult:
        """
        解决验证码
        
        Args:
            captcha_image: 验证码图片数据
            captcha_type: 验证码类型 (slider, click, rotate, etc.)
            
        Returns:
            CaptchaResult
        """
        raise NotImplementedError


class DdddOcrSolver(CaptchaSolver):
    """使用ddddocr本地识别（无需网络）"""
    
    def __init__(self):
        super().__init__()
        self.ocr = None
        self.det = None
        self._init_ocr()
    
    def _init_ocr(self):
        """初始化OCR引擎"""
        try:
            import ddddocr
            self.ocr = ddddocr.DdddOcr(show_ad=False)
            self.det = ddddocr.DdddOcr(det=True, show_ad=False)
            print("✅ ddddocr 初始化成功")
        except ImportError:
            print("⚠️ ddddocr 未安装，本地OCR不可用")
            print("   安装命令: pip install ddddocr")
        except Exception as e:
            print(f"⚠️ ddddocr 初始化失败: {e}")
    
    async def solve(self, captcha_image: bytes, captcha_type: str) -> CaptchaResult:
        """识别验证码"""
        if not self.ocr:
            return CaptchaResult(
                success=False,
                solution=None,
                cost_time=0,
                error_message="OCR引擎未初始化"
            )
        
        start_time = time.time()
        
        try:
            if captcha_type == 'text':
                # 文字验证码
                result = self.ocr.classification(captcha_image)
                return CaptchaResult(
                    success=True,
                    solution={'text': result},
                    cost_time=time.time() - start_time
                )
            
            elif captcha_type == 'detection':
                # 目标检测（用于滑块验证码找缺口）
                result = self.det.detection(captcha_image)
                return CaptchaResult(
                    success=True,
                    solution={'positions': result},
                    cost_time=time.time() - start_time
                )
            
            else:
                return CaptchaResult(
                    success=False,
                    solution=None,
                    cost_time=time.time() - start_time,
                    error_message=f"不支持的验证码类型: {captcha_type}"
                )
                
        except Exception as e:
            return CaptchaResult(
                success=False,
                solution=None,
                cost_time=time.time() - start_time,
                error_message=str(e)
            )


class TwoCaptchaSolver(CaptchaSolver):
    """2captcha.com 打码平台"""
    
    API_URL = "http://2captcha.com"
    
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
    
    async def solve(self, captcha_image: bytes, captcha_type: str) -> CaptchaResult:
        """提交验证码到2captcha"""
        import aiohttp
        
        start_time = time.time()
        
        try:
            # 上传验证码
            async with aiohttp.ClientSession() as session:
                data = aiohttp.FormData()
                data.add_field('method', 'base64')
                data.add_field('key', self.api_key)
                data.add_field('body', base64.b64encode(captcha_image).decode())
                
                if captcha_type == 'text':
                    data.add_field('textinstructions', '请输入图片中的文字')
                
                async with session.post(
                    f"{self.API_URL}/in.php",
                    data=data
                ) as response:
                    result = await response.text()
                    
                    if not result.startswith('OK|'):
                        return CaptchaResult(
                            success=False,
                            solution=None,
                            cost_time=time.time() - start_time,
                            error_message=f"提交失败: {result}"
                        )
                    
                    captcha_id = result.split('|')[1]
            
            # 轮询结果
            solution = await self._poll_result(captcha_id)
            
            return CaptchaResult(
                success=solution is not None,
                solution={'text': solution} if solution else None,
                cost_time=time.time() - start_time,
                error_message=None if solution else "识别超时"
            )
            
        except Exception as e:
            return CaptchaResult(
                success=False,
                solution=None,
                cost_time=time.time() - start_time,
                error_message=str(e)
            )
    
    async def _poll_result(self, captcha_id: str, max_wait: int = 120) -> Optional[str]:
        """轮询识别结果"""
        import aiohttp
        
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            while time.time() - start_time < max_wait:
                async with session.get(
                    f"{self.API_URL}/res.php",
                    params={
                        'key': self.api_key,
                        'action': 'get',
                        'id': captcha_id
                    }
                ) as response:
                    result = await response.text()
                    
                    if result == 'CAPCHA_NOT_READY':
                        await asyncio.sleep(5)
                        continue
                    
                    if result.startswith('OK|'):
                        return result.split('|')[1]
                    
                    # 错误
                    return None
        
        return None


class SliderCaptchaSolver:
    """滑块验证码专用解决器"""
    
    def __init__(self, use_ocr: bool = True, api_key: Optional[str] = None):
        self.use_ocr = use_ocr
        self.api_key = api_key
        self.ocr_solver = DdddOcrSolver() if use_ocr else None
        self.api_solver = TwoCaptchaSolver(api_key) if api_key else None
    
    async def solve_by_image_match(self, 
                                   background_image: bytes, 
                                   slider_image: bytes) -> CaptchaResult:
        """
        通过图像匹配找缺口位置
        
        Args:
            background_image: 背景图（带缺口）
            slider_image: 滑块图
            
        Returns:
            缺口位置x坐标
        """
        start_time = time.time()
        
        try:
            # 使用OpenCV进行模板匹配
            import cv2
            import numpy as np
            
            # 读取图片
            bg_array = np.frombuffer(background_image, np.uint8)
            slider_array = np.frombuffer(slider_image, np.uint8)
            
            bg = cv2.imdecode(bg_array, cv2.IMREAD_COLOR)
            slider = cv2.imdecode(slider_array, cv2.IMREAD_COLOR)
            
            # 模板匹配
            result = cv2.matchTemplate(bg, slider, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # 缺口位置
            gap_x = max_loc[0]
            
            return CaptchaResult(
                success=True,
                solution={'x': gap_x, 'confidence': max_val},
                cost_time=time.time() - start_time
            )
            
        except Exception as e:
            return CaptchaResult(
                success=False,
                solution=None,
                cost_time=time.time() - start_time,
                error_message=str(e)
            )
    
    async def solve_by_edge_detection(self, background_image: bytes) -> CaptchaResult:
        """通过边缘检测找缺口"""
        start_time = time.time()
        
        try:
            import cv2
            import numpy as np
            
            # 读取图片
            bg_array = np.frombuffer(background_image, np.uint8)
            bg = cv2.imdecode(bg_array, cv2.IMREAD_COLOR)
            
            # 转换为灰度图
            gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
            
            # 边缘检测
            edges = cv2.Canny(gray, 50, 150)
            
            # 找轮廓
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # 找最可能是缺口的轮廓（面积适中、位置合适）
            best_contour = None
            best_score = 0
            
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                area = w * h
                
                # 缺口通常在一定大小范围内
                if 1000 < area < 10000:
                    # 评分：面积适中、位置在右侧
                    score = area * (x / bg.shape[1])
                    if score > best_score:
                        best_score = score
                        best_contour = (x, y, w, h)
            
            if best_contour:
                x, y, w, h = best_contour
                return CaptchaResult(
                    success=True,
                    solution={'x': x, 'y': y, 'width': w, 'height': h},
                    cost_time=time.time() - start_time
                )
            else:
                return CaptchaResult(
                    success=False,
                    solution=None,
                    cost_time=time.time() - start_time,
                    error_message="未找到缺口"
                )
                
        except Exception as e:
            return CaptchaResult(
                success=False,
                solution=None,
                cost_time=time.time() - start_time,
                error_message=str(e)
            )
    
    def generate_slide_track(self, distance: int) -> List[Dict]:
        """
        生成滑块移动轨迹（模拟人类）
        
        Args:
            distance: 需要移动的距离
            
        Returns:
            轨迹点列表 [{x, y, time}]
        """
        track = []
        current = 0
        mid = distance * 3 / 4
        t = 0.2
        v = 0
        
        while current < distance:
            if current < mid:
                a = 2  # 加速
            else:
                a = -3  # 减速
            
            v0 = v
            v = v0 + a * t
            move = v0 * t + 0.5 * a * t * t
            current += move
            
            # 添加随机偏移
            y_offset = random.randint(-2, 2)
            
            track.append({
                'x': int(current),
                'y': y_offset,
                'time': int(t * 1000)
            })
        
        return track


class CaptchaHandler:
    """验证码处理主类 - 集成多种解决方案"""
    
    def __init__(self, 
                 use_local_ocr: bool = True,
                 api_key: Optional[str] = None):
        """
        初始化验证码处理器
        
        Args:
            use_local_ocr: 是否使用本地OCR (ddddocr)
            api_key: 打码平台API Key (2captcha等)
        """
        self.use_local_ocr = use_local_ocr
        self.api_key = api_key
        
        self.solvers = []
        
        # 本地OCR
        if use_local_ocr:
            self.solvers.append(('local', DdddOcrSolver()))
        
        # 打码平台
        if api_key:
            self.solvers.append(('api', TwoCaptchaSolver(api_key)))
    
    async def solve_captcha(self, 
                           captcha_image: bytes, 
                           captcha_type: str = 'text') -> CaptchaResult:
        """
        自动选择最佳方案解决验证码
        
        Args:
            captcha_image: 验证码图片
            captcha_type: 验证码类型
            
        Returns:
            CaptchaResult
        """
        # 优先尝试本地OCR
        for name, solver in self.solvers:
            print(f"尝试使用 {name} 解决验证码...")
            
            result = await solver.solve(captcha_image, captcha_type)
            
            if result.success:
                print(f"✅ {name} 识别成功，耗时 {result.cost_time:.2f}s")
                return result
            else:
                print(f"❌ {name} 识别失败: {result.error_message}")
        
        # 所有方案都失败
        return CaptchaResult(
            success=False,
            solution=None,
            cost_time=0,
            error_message="所有识别方案都失败"
        )
    
    async def solve_slider(self,
                          background_image: bytes,
                          slider_image: Optional[bytes] = None) -> CaptchaResult:
        """
        解决滑块验证码
        
        Args:
            background_image: 背景图
            slider_image: 滑块图（可选）
            
        Returns:
            缺口位置
        """
        solver = SliderCaptchaSolver()
        
        # 如果有滑块图，使用模板匹配
        if slider_image:
            return await solver.solve_by_image_match(background_image, slider_image)
        
        # 否则使用边缘检测
        return await solver.solve_by_edge_detection(background_image)


# 使用示例
async def demo():
    """验证码处理演示"""
    
    # 创建处理器
    handler = CaptchaHandler(use_local_ocr=True)
    
    # 示例：识别文字验证码
    # with open('captcha.png', 'rb') as f:
    #     image_data = f.read()
    # result = await handler.solve_captcha(image_data, 'text')
    # print(result)
    
    print("验证码处理模块已加载")
    print("支持功能:")
    print("  - 本地OCR识别 (ddddocr)")
    print("  - 打码平台 (2captcha)")
    print("  - 滑块验证码识别")
    print("  - 轨迹生成")


if __name__ == '__main__':
    import random
    asyncio.run(demo())
