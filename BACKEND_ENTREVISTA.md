# Ejercicio: Open Source y Calentamiento global

## El ejercicio

Queremos ver si existe una correlación entre la creación de proyectos Open Source
y el aumento de temperaturas.

El ejercicio consiste en crear una API REST que tiene un solo endpoint. Este recibe
como único parámetro un `username` de un usuario de GitHub y retorna un JSON con
2 datos: `Cantidad de repos` y `Temperatura promedio` de los días en los que ese
usuario creó repos.

La idea es usar la API de GitHub para obtener la ubicación del usuario y sus repos
para ir a alguna API de clima y traer la temperatura promedio del día de creación
de cada repo.

El ejercicio se puede realizar en cualquier lenguaje de programación siempre y
cuando se especifiquen los pasos de instalación y ejecución del programa.

## Entregables

- Repositorio de código y tests
- Archivo de documentación de la API

## Puntos extra

- Caching de la información en una DB local
- Explicación de decisiones a la hora de armar la API en el archivo de docs

## Recursos

- Obtener info de un [usuario de GitHub](https://api.github.com/users/:username)
- [Repos del usuario](https://api.github.com/users/:username/repos)
- Una [API de clima](https://developer.worldweatheronline.com/api/historical-weather-api.aspx) que tiene historial (Requiere API Key, tiene free trial)
