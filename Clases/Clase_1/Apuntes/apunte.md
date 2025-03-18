# Resumen de Computación II - Control de Versiones y Fundamentos

## 1. Configuración de Git
### Teoría
- **Git**: Sistema de control de versiones distribuido.
- **Importancia**: 
  - Colaboración sin conflictos.
  - Historial completo de cambios.
  - Capacidad de revertir errores.

### Práctica
```bash
# Verificar instalación
git --version

# Configurar identidad
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

---

## 2. Creación de Repositorio
### Conceptos clave
- **Repositorio local**: Directorio con `.git` para historial.
- **Repositorio remoto**: Plataformas como GitHub/GitLab.

### Comandos
```bash
# Inicializar repositorio
mkdir Computacion_II && cd Computacion_II
git init

# Verificar estado
git status
```

---

## 3. Estructura del Repositorio
### Directorios requeridos
```bash
.
├── README.md
├── TP_1
├── TP_2
├── Clases
│   └── Clase_1
│       ├── Apuntes
│       ├── Ejercicios
│       └── Resumen_pedagógico
└── TRABAJO_FINAL
```

### Contenido mínimo de `README.md`
```markdown
# [Tu Nombre]
## Expectativas
- Dominar Git y workflows profesionales
## Intereses
- Desarrollo backend
- Automatización
## Hobbies
- Fotografía
- Ajedrez
```

---

## 4. Primer Commit y Flujo de Trabajo
### Ciclo de Git
1. Área de trabajo → `git add` → Staging → `git commit` → Repositorio

### Comandos clave
```bash
# Añadir todos los archivos
git add .

# Commit inicial
git commit -m "Primer commit: estructura inicial"

# Ver historial
git log
```

---

## 5. Conexión con Repositorio Remoto
### Configuración
```bash
# Vincular repositorio local con remoto
git remote add origin https://github.com/tu-usuario/repositorio.git

# Subir cambios
git push -u origin main
```

### Cambiar de `master` a `main`
```bash
# Renombrar rama local
git branch -m master main

# Actualizar remoto
git push -u origin main
git push origin --delete master
```

---

## 6. Configuración SSH
### Generar clave
```bash
ssh-keygen -t rsa -b 4096 -C "tu@email.com"
```

### Vincular con GitHub/GitLab
1. Copiar clave pública:
```bash
cat ~/.ssh/id_rsa.pub
```
2. Pegar en **Settings → SSH and GPG keys**.

### Usar SSH en repositorios
```bash
git remote set-url origin git@github.com:tu-usuario/repositorio.git
```

---

## 7. Conceptos Unix
### Redirección y Pipes
```bash
# Redirigir salida
ls -l > listado.txt

# Pipe entre comandos
cat archivo.txt | grep "palabra"
```

### Archivos especiales
- `/dev/null`: "Agujero negro" para descartar salidas
- `2>`: Redirigir errores

---

# Ejercicios de Verificación
1. Crea un repositorio desde cero con la estructura requerida.
2. Configura SSH y clona tu repositorio.
3. Haz un cambio en el README y sincronízalo con el remoto usando:
```bash
git add README.md
git commit -m "Actualización de perfil"
git push
```

# Recursos Adicionales
- [Git Documentation](https://git-scm.com/doc)
- [GitHub SSH Guide](https://docs.github.com/es/authentication/connecting-to-github-with-ssh)

