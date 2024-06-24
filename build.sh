#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

echo "Рабочая директория: $DIR"

echo "Сборка фронтенда.."
docker build --no-cache -t ngw_kpt-front:1.0.0 ./frontend

echo "Сборка бэкенда.."
docker build --no-cache -t ngw_kpt-back:1.0.0 ./backend

echo "Сборка завершена."
echo "---------------------------------"

echo "Сохранение образов.."
docker save ngw_kpt-front:1.0.0 | gzip > ./share/ngw_kpt-front.tar.gz
docker save ngw_kpt-back:1.0.0 | gzip > ./share/ngw_kpt-back.tar.gz

echo "Сохранение завершено."
