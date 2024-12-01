# Etapa 1: Construcción de dependencias del sistema y compilación de OpenMVS y COLMAP
FROM nvidia/cuda:11.8-devel-ubuntu20.04 AS builder

# Evitar prompts durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Actualizar sistema e instalar dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    cmake \
    ninja-build \
    build-essential \
    libboost-program-options-dev \
    libboost-graph-dev \
    libboost-system-dev \
    libeigen3-dev \
    libflann-dev \
    libfreeimage-dev \
    libmetis-dev \
    libgoogle-glog-dev \
    libgtest-dev \
    libgmock-dev \
    libsqlite3-dev \
    libglew-dev \
    qtbase5-dev \
    libqt5opengl5-dev \
    libcgal-dev \
    libceres-dev \
    libopencv-dev \
    libboost-iostreams-dev \
    libboost-serialization-dev \
    libpng-dev \
    libjpeg-dev \
    libtiff-dev \
    libglu1-mesa-dev \
    nvidia-cuda-toolkit \
    nvidia-cuda-toolkit-gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Clonar y compilar COLMAP
WORKDIR /opt
RUN git clone https://github.com/colmap/colmap.git \
    && cd colmap \
    && git checkout dev \
    && mkdir build \
    && cd build \
    && cmake .. -DCMAKE_BUILD_TYPE=Release -DCUDA_ARCH_BIN=7.5 -DENABLE_CUDA=ON \
    && make -j$(nproc) \
    && make install

# Clonar y compilar VCGLib y OpenMVS
RUN git clone https://github.com/cdcseacave/VCG.git vcglib \
    && git clone https://github.com/cdcseacave/openMVS.git openMVS \
    && mkdir openMVS_build \
    && cd openMVS_build \
    && cmake ../openMVS -DCMAKE_BUILD_TYPE=Release -DVCG_ROOT="/opt/vcglib" \
    && make -j$(nproc) \
    && make install

# Etapa 2: Crear la imagen final para ejecutar el proyecto
FROM python:3.9-slim

# Copiar herramientas compiladas desde la etapa anterior
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib /usr/local/lib

# Configurar el entorno de trabajo
WORKDIR /app

# Instalar dependencias de Python y OpenCV
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopencv-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Comando para ejecutar la API
CMD ["python", "api.py"]
