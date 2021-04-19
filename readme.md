El programa tiene la funcion de facilitar el etiquetado de imagenes satelitales provenientes de AMAZON S3


La configuracion es sencilla, primero es abrir el archivo info.json y colocar las credenciales necesarias de AMAZON y ademas indicar que bucket va a entrar,
despues, el archivo o carpeta que contenga todas las imagenes satelitales, cambiar el estado de "existe" a falso, con el fin de que cree un csv donde estara toda las etiquetas colocadas, y por ultimo, el indice inicializarlo en 0, este es una referencia de que imagen se quedo en el software para que asi si se vuelve a abrir, abra desde la ultima en la que se utilizo, y podra etiquetar hasta terminar toda esa carpeta.


Ejecute tycho.py

Si quiere cambiar a otra carpeta u otro bucket solo repita lo mismo de arriba, con info, reinice el "indice","existe", y que "archivo" apunte al correspodiente, el software hara su trabajo solicito para filtrar la informacion.



El software puede utilizarse con click en los botones o utilizando la teclas de izquierda y derecha, y espacio para marcar la imagen