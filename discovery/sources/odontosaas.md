# OdontoSaaS

- **URL**: https://odontosaas.com/
- **Fecha de investigación**: 2026-10-15

## Problema que resuelve

Según su meta description: "OdontoSaaS - Sistema odontológico completo para gestão de clínicas. Agenda inteligente, prontuário digital, financeiro, marketing e IA." El título OG apunta a "Aumente o faturamento da sua clínica com agenda inteligente, marketing automatizado e IA."

## Usuarios objetivo

(no publicado). El sitio está en portugués (pt-BR, precios en BRL), por lo que apunta al mercado de Brasil. No se pudo recuperar del HTML shell la descripción de segmentos/roles objetivo.

## Features detectadas

- Agenda inteligente (mencionada en meta description y keywords)
- Prontuario digital / prontuário eletrônico
- Módulo financeiro
- Marketing automatizado
- IA (asistente/inteligencia artificial)
- CRM odontológico (según keywords del sitio)

(Detalle funcional no recuperable: el contenido real se renderiza con JavaScript y no fue accesible vía fetch.)

## Pricing

(no publicado). El único dato recuperable del sitio es un JSON-LD que declara "Teste grátis por 7 días" (precio 0, BRL). No se obtuvieron planes ni cifras concretas.

## Posicionamiento

"Sistema odontológico completo para gestão de clínicas" (título del sitio). Se posiciona en torno a la completitud del sistema y el uso de IA. Título de marca: "OdontoSaaS - Sistema de Gestao para Clinicas Odontologicas".

## Diferenciadores

(no publicado). El HTML no expone su discurso diferencial; sólo etiquetas de marketing ("completo", "inteligente", "IA"). No se puede afirmar nada más sin inventar.

## Notas del investigador

- **Limitación de fetch**: `odontosaas.com` es una SPA (React) — el HTML servido sólo contiene el `#root` vacío y las etiquetas `<meta>`/JSON-LD. El contenido visible (planes, funcionalidades, precios) se carga por JavaScript y no fue accesible vía webfetch. Se intentaron también `https://odontosaas.com/precos`, `/planos` y `/funcionalidades` (todas devolvieron el mismo shell sin datos) y se usó la herramienta de búsqueda web sin obtener contenido de valor del dominio.
- Por eso, varios campos quedan en `(no publicado)` en lugar de inventar datos.
- Ojo: en resultados de búsqueda apareció contenido de un sitio distinto (**DentalSaaS**, `dentalsaas.drbsolucoes.com.br`, con planes de R$ 147 / R$ 297) mezclado cerca del resultado de OdontoSaaS. NO corresponde a OdontoSaaS y no se usó.
- Riesgo para discovery: es un competidor brasileño de mercado/perfil incierto (posible clon/plantilla SaaS). Se recomienda re-verificar con un fetch que ejecute JS (navegador headless) antes de sacar conclusiones.
