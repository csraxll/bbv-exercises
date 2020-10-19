# bbv-exercises

Ejercicios de scrapping sobre la plataforma Netflix. Se extrae la información de un título disponible en la plataforma.
Hay dos variantes, una en forma de script plano que parsea la información a un diccionario y otra más orientada a objetos que vuelca la información recolectada a una estructura de clases.

Los ejercicios fueron desarrollados y probados con la versión 3.8.5 de Python

# Instalación de dependencias
Las unicas dependencias del proyecto son BeautifulSoup4 y requests

> pip install -r requeriments.txt

# Uso
Tanto scrapping-exercise.py como scrapping-exercise.py soportan una url como argumento al ser ejecutados.
El argumento debe ser de la forma:

https://www.netflix.com/ar/title/70143836

Donde lo único que puede cambiar es el denominador de país (ar) y el identificador del título (70413836)
Por ejemplo, se pueden ejecutar los scripts de las siguientes maneras:


> python scrapping-exercise.py https://www.netflix.com/ar/title/70143836


Sin denominador de país
> python scrapping-exercise.py https://www.netflix.com/title/70143836


Con otros títulos
> python scrapping-exercise.py https://www.netflix.com/ar/title/80149395

Por defecto, si no se ejecutan los scripts con una url como parámetro se muestran los resultados para el título Breaking Bad de Argentina.
