# Portafolio de Susana Tralma

Actualizado el 12 de noviembre de 2026 sobre el ZIP adjunto: inicio responsive y centrado en móvil, nuevo bloque de contacto y botón de Calendly.

## Contenido
- `dist/`: sitio completo listo para servir, con HTML, CSS, JavaScript, imágenes, fuentes y videos.
- Archivos Python, JSON, CSS y plantillas en la raíz: fuentes para editar y regenerar el sitio.
- `.github/workflows/pages.yml`: publicación opcional de `dist/` en GitHub Pages.

## Subir el código a GitHub
Descomprime este ZIP. Crea un repositorio vacío en tu cuenta de GitHub. Abre una terminal en la carpeta descomprimida y ejecuta estos comandos sustituyendo TU_USUARIO y TU_REPOSITORIO:

```bash
git init
git add .
git commit -m "Agregar portafolio de Susana Tralma"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git push -u origin main
```
GitHub puede solicitar iniciar sesión. No subas el ZIP como único archivo: sube su contenido descomprimido. La carpeta `.github` está oculta en algunos sistemas y también debe incluirse.

## Vista local
Con Python 3 instalado, desde la carpeta del proyecto:

```bash
python3 -m http.server 8000 --directory dist
```
Abre http://localhost:8000.

## Editar y regenerar
El sitio ya está compilado y no necesita instalar dependencias para publicarlo. Para regenerarlo después de modificar las fuentes:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -B build.py
```
En Windows, activa el entorno con `.venv\Scripts\activate`.
Los archivos `*_page.py` y los JSON contienen contenido, y `dist/` también contiene estilos y recursos que usa la compilación: no borres esta carpeta. El proceso convierte los PNG de `dist/assets/` a WebP; referencia la extensión WebP en las páginas.

## Publicación opcional
El flujo incluido publica la carpeta `dist/` usando GitHub Pages al enviar cambios a `main`, si Pages está configurado para GitHub Actions. Guardar el código en GitHub no requiere activar Pages. La disponibilidad de Pages depende de la configuración y visibilidad del repositorio.

Se excluyen el historial Git y la configuración específica del alojamiento anterior. Esta copia no modifica el sitio publicado.

## Adaptación responsive
Todas las páginas cargan `dist/responsive.css` al final. Ajustes para tablet (1024 px), móvil (800 px) y pantallas pequeñas (600 px). En móvil: títulos principales 28–36 px, títulos de sección 24–30 px, subtítulos 20–24 px y cuerpo 16 px; controles táctiles de al menos 44 px. Los casos extensos mantienen el texto alineado a la izquierda.
