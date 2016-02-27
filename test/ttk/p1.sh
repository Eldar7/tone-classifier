#!/bin/bash
# Скрипт вычисления результатов для контеста

svm="../../svm/"
log="log.txt"
res="result"

set -o xtrace

# Создаем каталог с результатом работы
mkdir -p $res

for f in 1 2 3 4 5;
do
    echo "Test type: $f"
    # Копируем результаты настроек классификатора
    cp $f/*.conf $svm

    pushd .
        cd $svm
        echo "Apply 2016 model"
        make 16_tf_idf_ttk_balanced | grep "F_R" >> $f.res
    popd

    # Создаем каталог с результатами
    out="./$res/$f/"
    mkdir $out

    # Копируем все конфигурации, которые использовались при тестировании
    confs="msg.conf"
    cp "$svm$confs" "$out"
    confs="features.conf"
    cp "$svm$confs" "$out"

    # Копируем ответ
    mv "$svm$f.res" "$out"
done
