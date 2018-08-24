# OpenWarming
Ejercicio técnico para **Brubank**

### Decisiones de diseño
La API fue realizada en Python facilidad que posee el lenguaje para construir aplicaciones 
(tipado dinámico, facilidad para construir módulos, bibliotecas de casi todo). La API
fue implementada usando la biblioteca (Tornado)[http://www.tornadoweb.org/en/stable/]. Hay algunas otras alternativas interesantes a la misma (Flask, Djnago, etc.), pero debido a que ya había utilizado esta antes, y a que requiere muy poco código boilerplate, opté por la misma. Como RESTClient, se utilizó la biblioteca (Requests)[http://docs.python-requests.org/en/master/].

La respuesta de la API consiste en la cantidad de repositorios del usuario solicitado, y una lista con las temperaturas de la fecha de creación de cada repo. Había posibles respuestas:
- La media de todas las temperaturas.
- Una lista con la temperatura media de cada fecha.
Debido a que la funcionalidad de la API (el motivo) es *demostrar* la relación calentamiento global - open source, tiene más sentido mostrar los valores individuales de temperatura, de forma de mostrar la variación de las temperaturas.

En cualquiera de los request que se hace (buscar la ubicación del usuario, traer la fecha de creación de los repositorios, u obtener la temperatura media en cada una de esas fechas) se optó por devolver un código de error (404 o 500), dependiendo del caso. Las razones por las cuales se eligió esto son:
- En caso que el request que fallé sean los correspondiente a la API de Github, no se estaría encontrando correctamente ni la ubicación del usuario, lo caul haría que la funcionalida del endpoint pierda sentido; o no se pueda recuperar las fechas de creación de los repositorios, lo cual de igual manera, causaría lo mismo.
- En el caso en el que se busca obtener la información climática de cada fecha, se podría optar por omitir que falle alguno de los request, y de esta mantera devolver una lista incompleta de temperaturas. Debido a que esto causaría una incongruencia con la cantidad de repositorios que también está en la respuesta (ya que sería una media calculada con menos datos), se optó por fallar.

El diseño de la API consiste en una clase principal, Server, la cual posee la lógica para instanciar en servidor en si, bindearlo a un puerto (8888 por default, facilmente cambiable (aca)[https://github.com/plbalbi/openwarming/blob/master/main.py]). Luego, el handler del endpoint esta definido dentro de su propia clase, la cual subclasifica a los Hanlders proveídos por Tornado. Para no tener la lógica de obtener la info. del usuario solicitado de Github, y la info. climática, estas fueron separadas en dos services:
- **weather_service** (Por ahora quedó la API_KEY aca, esto claramente debería ser cambiado a una variable de ambiente del equipo donde se corre el servido, o que el mismo la tome como parámetro. Queda como un TODO)
- **github_service**

En estos esta definido los métodos correspondiente a la info que es necesario recuperar de cada API, pero no hay un objeto que represente los servicios en si. Esto es debido a que los mismos son stateless por el momento (si se agregara algún tipo de caching, que posiblemente convenga a wather service, habría que definir un objeto que represente al mismo, y que sea colaborador de la cache utilizada para el mismo).

A lo largo del proyecto hay **TODO's** definidos. Son cambios que debería hacer como siguientes iteraciones al mismo.

### Requerimientos
- Python 3.7.0
- Instalar dependencias con ```pip install -u -r requirements.txt```

### Ejecución
Para ejecutar la API, correr ```python main.py```.

Para correr el test suite, correr ```./test.sh```