# Network Monitor

## Descripción del Proyecto

Sistema de monitoreo de red doméstica que utiliza una Raspberry Pi 4 como nodo de escaneo, GitHub Actions para procesamiento y automatización, y Streamlit Community Cloud para visualización. El proyecto tiene un objetivo dual: crear una herramienta útil de monitoreo y servir como vehículo de aprendizaje progresivo de GitHub Actions.

## Objetivos

### Objetivo Principal
Construir un pipeline automatizado que detecte dispositivos en una red local, almacene el historial de escaneos, y presente los datos en un dashboard interactivo accesible desde cualquier lugar.

### Objetivo de Aprendizaje
Dominar GitHub Actions de forma progresiva, partiendo desde workflows básicos hasta configuraciones avanzadas que incluyan cron jobs, manejo de secretos, artifacts, GitHub Pages, y notificaciones.

## Arquitectura del Sistema

```
┌─────────────────┐     push JSON      ┌─────────────────┐
│  Raspberry Pi   │ ─────────────────► │     GitHub      │
│  (Scanner)      │                    │   Repository    │
└─────────────────┘                    └────────┬────────┘
                                                │
                                                │ trigger
                                                ▼
                                       ┌─────────────────┐
                                       │  GitHub Actions │
                                       │   (Workflows)   │
                                       └────────┬────────┘
                                                │
                                                │ deploy
                                                ▼
                                       ┌─────────────────┐
                                       │    Streamlit    │
                                       │  Community Cloud│
                                       └─────────────────┘
```

### Flujo de Datos

1. La Raspberry Pi ejecuta un escaneo de red periódicamente (cron job local)
2. Los resultados se guardan en formato JSON y se hace push al repositorio
3. GitHub Actions detecta el cambio y ejecuta workflows de validación y procesamiento
4. Streamlit Community Cloud detecta cambios en el repo y redespliega el dashboard automáticamente
5. El usuario accede al dashboard desde cualquier navegador

## Tecnologías

### Hardware
- **Raspberry Pi 4** — Nodo de escaneo conectado a la red local vía WiFi
- **Sistema Operativo** — Raspberry Pi OS

### Escaneo de Red
- **arp-scan** — Herramienta de línea de comandos para descubrimiento de dispositivos via ARP
- **Python 3** — Lenguaje para el script de escaneo y procesamiento

### Control de Versiones y CI/CD
- **Git** — Control de versiones
- **GitHub** — Repositorio remoto
- **GitHub Actions** — Automatización de workflows

### Visualización
- **Streamlit** — Framework para el dashboard interactivo
- **Streamlit Community Cloud** — Hosting gratuito para apps de Streamlit

### Librerías Python
- **subprocess** — Ejecución de comandos del sistema (arp-scan)
- **json** — Serialización de datos
- **datetime** — Timestamps de escaneos
- **pandas** — Manipulación de datos para el dashboard
- **streamlit** — Construcción del dashboard

## Estructura del Repositorio

```
network-monitor/
├── .github/
│   └── workflows/
│       ├── validate.yml        # Fase 3: Validación de JSON
│       ├── process.yml         # Fase 4: Procesamiento de datos
│       └── notify.yml          # Fase 7: Alertas y notificaciones
├── scanner/
│   ├── scanner.py              # Script principal de escaneo
│   ├── config.py               # Configuración del scanner
│   └── requirements.txt        # Dependencias del scanner
├── dashboard/
│   ├── app.py                  # Aplicación Streamlit
│   ├── utils.py                # Funciones auxiliares
│   └── requirements.txt        # Dependencias del dashboard
├── data/
│   ├── scan_results.json       # Último escaneo (actualizado por la Pi)
│   └── history/                # Histórico de escaneos (generado por Actions)
│       └── .gitkeep
├── docs/
│   └── setup-raspberry.md      # Guía de configuración de la Pi
├── PROJECT.md                  # Este archivo
├── README.md                   # Documentación pública del proyecto
└── .gitignore
```

## Fases del Proyecto

### Fase 1: El Script Explorador
**Objetivo:** Crear un script funcional que detecte dispositivos en la red local.

**Tareas:**
- [ ] Instalar arp-scan en la Raspberry Pi
- [ ] Crear script Python que ejecute arp-scan y parsee la salida
- [ ] Generar archivo JSON estructurado con los resultados
- [ ] Probar el script manualmente y validar resultados

**Entregables:**
- `scanner/scanner.py` funcionando en la Pi
- `data/scan_results.json` generado correctamente

**Conceptos de GitHub Actions:** Ninguno todavía.

---

### Fase 2: Conexión con GitHub
**Objetivo:** Configurar la Pi para que pueda hacer push automático al repositorio.

**Tareas:**
- [ ] Crear repositorio en GitHub
- [ ] Configurar Git en la Raspberry Pi
- [ ] Generar Personal Access Token (PAT) o configurar SSH keys
- [ ] Modificar el script para hacer commit y push después del escaneo
- [ ] Probar el flujo completo manualmente

**Entregables:**
- Repositorio creado y clonado en la Pi
- Script modificado con capacidad de push
- Push exitoso desde la Pi al repo

**Conceptos de GitHub Actions:** Ninguno todavía, pero se prepara el terreno.

---

### Fase 3: Primer Workflow
**Objetivo:** Crear el primer workflow de GitHub Actions que valide los datos.

**Tareas:**
- [ ] Crear directorio `.github/workflows/`
- [ ] Escribir workflow `validate.yml` que se dispare en push a `data/`
- [ ] Agregar step que valide la estructura del JSON
- [ ] Agregar step que muestre resumen del escaneo en los logs
- [ ] Verificar ejecución exitosa en la pestaña Actions del repo

**Entregables:**
- `.github/workflows/validate.yml` funcionando
- Workflow ejecutándose automáticamente en cada push

**Conceptos de GitHub Actions:**
- Estructura básica de un workflow (name, on, jobs, steps)
- Evento `push` con filtro de paths
- Uso de `actions/checkout`
- Steps con `run` para ejecutar comandos
- Visualización de logs en GitHub

---

### Fase 4: Procesamiento de Datos
**Objetivo:** Procesar los datos del escaneo y preparar histórico.

**Tareas:**
- [ ] Crear workflow `process.yml` que se ejecute después de `validate.yml`
- [ ] Agregar step que copie el escaneo actual al directorio `history/` con timestamp
- [ ] Implementar script Python que agregue estadísticas básicas
- [ ] Usar artifacts para guardar los resultados procesados
- [ ] Hacer commit automático de los cambios al repo

**Entregables:**
- `.github/workflows/process.yml` funcionando
- Histórico de escaneos acumulándose en `data/history/`
- Artifacts disponibles en cada ejecución

**Conceptos de GitHub Actions:**
- Workflow dispatch y dependencias entre workflows
- Artifacts (upload-artifact, download-artifact)
- Commits automáticos desde Actions (usando un bot o PAT)
- Expresiones y contextos (`${{ github.sha }}`, etc.)

---

### Fase 5: Dashboard con Streamlit
**Objetivo:** Crear y desplegar el dashboard interactivo.

**Tareas:**
- [ ] Crear aplicación Streamlit básica que lea `scan_results.json`
- [ ] Mostrar tabla de dispositivos actuales
- [ ] Agregar gráfica de dispositivos en el tiempo (usando histórico)
- [ ] Conectar repositorio a Streamlit Community Cloud
- [ ] Verificar que el dashboard se actualice automáticamente

**Entregables:**
- `dashboard/app.py` funcionando localmente
- Dashboard desplegado en Streamlit Community Cloud
- URL pública accesible

**Conceptos de GitHub Actions:**
- Entender cómo Streamlit Cloud se integra con GitHub (no es Actions per se, pero complementa)
- Posible workflow para validar que la app de Streamlit no tenga errores de sintaxis

---

### Fase 6: Automatización Completa
**Objetivo:** Hacer que todo el sistema funcione sin intervención manual.

**Tareas:**
- [ ] Configurar cron job en la Raspberry Pi para ejecutar el scanner periódicamente
- [ ] Ajustar frecuencia de escaneo (cada hora, cada 30 minutos, etc.)
- [ ] Agregar manejo de errores y reintentos en el script
- [ ] Implementar logging local en la Pi para debugging
- [ ] Verificar que el pipeline completo funcione durante 24-48 horas

**Entregables:**
- Cron job configurado y funcionando
- Sistema operando de forma autónoma
- Logs de ejecución disponibles en la Pi

**Conceptos de GitHub Actions:**
- Workflows programados con cron (aunque aquí el cron está en la Pi)
- Opcional: workflow de "health check" que verifique que la Pi sigue reportando

---

### Fase 7: Alertas y Notificaciones
**Objetivo:** Agregar inteligencia al sistema para detectar eventos importantes.

**Tareas:**
- [ ] Implementar detección de dispositivos nuevos (no vistos antes)
- [ ] Implementar detección de dispositivos que desaparecieron
- [ ] Crear workflow que envíe notificación cuando hay cambios significativos
- [ ] Configurar destino de notificaciones (email, Slack, Telegram, o Discord)
- [ ] Agregar sección de "eventos recientes" al dashboard

**Entregables:**
- `.github/workflows/notify.yml` funcionando
- Notificaciones llegando cuando hay cambios en la red
- Dashboard mostrando historial de eventos

**Conceptos de GitHub Actions:**
- Condicionales en workflows (`if:`)
- Secrets para tokens de APIs externas
- Integración con servicios externos (webhooks)
- Matrices y estrategias (opcional, para notificar a múltiples canales)

---

## Extensiones Futuras (Opcionales)

Estas son ideas para continuar después de completar las 7 fases principales:

- **Identificación de dispositivos:** Mantener un archivo de "dispositivos conocidos" con nombres amigables (ej: "iPhone de Rodrigo", "Smart TV Sala")
- **Self-hosted runner:** Convertir la Pi en un runner de GitHub Actions para ejecutar workflows localmente
- **Geofencing:** Detectar cuándo ciertos dispositivos (teléfonos) entran o salen de la red
- **Métricas avanzadas:** Tiempo de actividad por dispositivo, patrones de uso, etc.
- **Multi-red:** Soportar múltiples Raspberry Pi en diferentes ubicaciones

## Recursos de Referencia

### GitHub Actions
- [Documentación oficial de GitHub Actions](https://docs.github.com/en/actions)
- [Sintaxis de workflows](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Eventos que disparan workflows](https://docs.github.com/en/actions/reference/events-that-trigger-workflows)
- [Marketplace de Actions](https://github.com/marketplace?type=actions)

### Streamlit
- [Documentación de Streamlit](https://docs.streamlit.io/)
- [Streamlit Community Cloud](https://streamlit.io/cloud)
- [Galería de ejemplos](https://streamlit.io/gallery)

### Raspberry Pi y Networking
- [Documentación de arp-scan](https://github.com/royhills/arp-scan)
- [Guía de SSH en Raspberry Pi](https://www.raspberrypi.com/documentation/computers/remote-access.html)

## Configuración del Entorno de Desarrollo

### En la Raspberry Pi
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar herramientas necesarias
sudo apt install arp-scan git python3-pip -y

# Clonar repositorio (después de crearlo)
git clone https://github.com/USERNAME/network-monitor.git
cd network-monitor

# Instalar dependencias del scanner
pip3 install -r scanner/requirements.txt
```

### Para desarrollo del dashboard (local)
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r dashboard/requirements.txt

# Ejecutar dashboard localmente
streamlit run dashboard/app.py
```

## Notas Importantes

1. **Seguridad:** El repositorio debe ser público para usar Streamlit Community Cloud gratis. No incluir información sensible en los datos (las MACs y IPs locales generalmente no son un riesgo, pero considerar qué información se expone).

2. **Rate limits:** GitHub tiene límites en la cantidad de commits por hora. El escaneo no debería ser más frecuente que cada 15-30 minutos para evitar problemas.

3. **Permisos:** El script de escaneo necesita `sudo` para ejecutar arp-scan. Configurar sudoers apropiadamente para el cron job.

4. **Conectividad:** Si la Pi pierde conexión WiFi, los escaneos fallarán. Considerar agregar reconexión automática o alertas de salud.
