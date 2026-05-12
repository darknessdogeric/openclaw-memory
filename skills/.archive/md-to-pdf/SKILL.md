# Markdown to PDF Converter Skill

Converte arquivos Markdown para PDF usando md-to-pdf com suporte a temas e estilos customizados.

## 🛠️ Ferramentas Registradas

### `md_to_pdf_convert`

Converte um arquivo Markdown para PDF.

**Parâmetros:**
- `inputFile` (string, obrigatório): Caminho do arquivo Markdown
- `outputFile` (string, opcional): Caminho do PDF de saída
- `theme` (string, opcional): Tema - "default", "github", "latex"
- `header` (string, opcional): Texto do cabeçalho
- `footer` (string, opcional): Texto do rodapé

**Exemplo:**
```json
{
  "inputFile": "/home/user/documento.md",
  "outputFile": "/home/user/documento.pdf",
  "theme": "github",
  "header": "Relatório Técnico",
  "footer": "Página {page} de {pages}"
}
```

### `md_to_pdf_batch`

Converte múltiplos arquivos Markdown em lote.

**Parâmetros:**
- `inputDir` (string, obrigatório): Diretório com arquivos Markdown
- `outputDir` (string, obrigatório): Diretório para PDFs de saída
- `pattern` (string, opcional): Padrão de arquivo (default: "*.md")

**Exemplo:**
```json
{
  "inputDir": "/home/user/documentos",
  "outputDir": "/home/user/pdfs",
  "pattern": "*.md"
}
```

## ⚙️ Configuração

Adicione ao seu `openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "openclaw-md-to-pdf": {
        "enabled": true,
        "config": {
          "defaultOutputDir": "./output",
          "defaultTheme": "github"
        }
      }
    }
  }
}
```

## 📦 Instalação

```bash
# Clonar repositório
git clone https://github.com/FelipeOFF/openclaw-md-to-pdf.git

# Instalar dependências
cd openclaw-md-to-pdf
npm install
```

## 🔧 Uso via CLI

```bash
# Converter arquivo
node scripts/convert.js documento.md

# Com tema
node scripts/convert.js documento.md --theme github

# Com cabeçalho/rodapé
node scripts/convert.js documento.md --header "Título" --footer "Página {page}"
```

## 🎨 Temas Disponíveis

- **default**: Estilo limpo e minimalista
- **github**: Estilo GitHub-flavored Markdown
- **latex**: Estilo acadêmico/LaTeX

## 📝 Requisitos

- Node.js >= 18.0.0
- **Chrome ou Chromium instalado** (requerido pelo Puppeteer)

### Instalando o Chrome/Chromium

Esta ferramenta requer Chrome/Chromium. O Puppeteer tentará baixar automaticamente, mas você pode precisar instalar manualmente:

**Opção 1: Automático (via Puppeteer)**
```bash
npx puppeteer browsers install chrome
```

**Opção 2: Gerenciador de pacotes do sistema**
```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# macOS
brew install chromium
```

**Opção 3: Variável de ambiente**
Se o Chrome estiver em local não padrão:
```bash
export PUPPETEER_EXECUTABLE_PATH=/caminho/para/chrome
```

## 🔧 Solução de Problemas

### Erro: "Cannot find module 'commander'"
```bash
npm install commander glob --save
```

### Erro: "Failed to launch browser" ou "No usable sandbox"
O Chrome pode não estar instalado. Instale usando um dos métodos acima.

### Erro: "Chrome executable not found"
Defina o caminho do Chrome explicitamente:
```bash
export PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
```

### Falha no download do Puppeteer
Se o Puppeteer falhar ao baixar o Chrome, pule e instale manualmente:
```bash
PUPPETEER_SKIP_DOWNLOAD=true npm install
# Depois instale o Chrome manualmente (veja Requisitos)
```

## 📄 Licença

MIT License - ver arquivo LICENSE

---

**Documentação em português para usuários brasileiros**
