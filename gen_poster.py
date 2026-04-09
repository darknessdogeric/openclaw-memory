# -*- coding: utf-8 -*-
import os
os.chdir(r"C:\Users\ericz\.openclaw\workspace")

html = open("test_poster.html", "r", encoding="utf-8").read()
print(f"HTML file has {len(html)} chars")
print("File exists:", os.path.exists("test_poster.html"))
