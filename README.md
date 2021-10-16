TUNOverIRC
====
TUNOverIRC - это виртуальный сетевой адаптер работающий через irc сеть.


Installing
----------

> sudo pip3 install python-pytun irc base91 multipledispatch

> git clone git@tomas.gl:TomasGl/tun-over-irc.git


Using
-----
На каждый клиент необходимо склонировать данный репозиторий. Открыть файл config.conf и настроить адресацию и используемый irc сервер. В конечном итоге запустить программу на обоих машинах командой: 
> sudo python3 main.py

Можете проверить пинг:)


TODO
----
Выводить ошибку, если ip занят
