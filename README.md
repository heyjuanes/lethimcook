Computación en la Nube
Jhorman A. Villanueva Vivas
Práctica 4-Implementar un entorno Multi-Container altamente disponible en AWS
para una aplicación de IA
Objetivos.
• Configurar contenedores para una aplicación de IA en un entorno altamente
disponible en instancias en AWS.
Procedimiento.
1. Configurar la infraestructura de red con dos zonas de disponibilidad y subredes
públicas y privadas. Las subredes privadas deben tener salida a internet.
Presentar un esquema de la infraestructura a implementar.
2. Lanzar en las subredes privadas al menos dos instancias EC2 en zonas de
disponibilidad diferentes.
3. Instale Docker en las instancias.
a. Cree un usuario de sistema sin privilegios root. Realice la respectiva
configuración para que este usuario puede ejecutar contenedores sin usar
sudo. La implementación de los contenedores debe realizarse bajo la
sesión de este usuario.
b. Recuerde usar el User Data
4. Implementar a través de contenedores una aplicación de IA (clasificador de
imágenes, predicción, análisis de sentimientos, etc) que cumpla con un caso
específico. Estos contenedores deben ir en las instancias que están en por lo
menos dos zonas de disponibilidad diferentes. La imagen del contener debe
estar alojada en Docker Hub.
5. La aplicación debe ser accesible desde internet.
6. Lance a través de otro contenedor (solo uno que puede ir en cualquier de las
intancias) una base de datos (PostgreSQL, MySQL, MongoDB, etc) donde la
aplicación va a guardar información. Asegúrese de que las instancias puedan
comunicarse entre sí a través de sus IPs privadas y que el Security Group
permita el tráfico en el puerto de la base de datos. Use una configuración MultiContainer con Docker-Compose.
7. Debe aplicar la política de mínimos privilegios a través de los Security Group
(Grupos de seguridad).
8. El acceso a la aplicación web se realizar a través de una balanceador de carga.
9. Realice pruebas que confirmen la alta disponibilidad.
10.Alojar el código de la aplicación de IA, Dockerfile, Docker-Compose, entre otros,
en un repositorio de GitHub.
a. Documente el paso a paso a través de un README.
11.Presentar implementación frente a compañeros. 
