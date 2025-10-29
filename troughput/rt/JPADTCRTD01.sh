#!/usr/bin/expect -f


set timeout 180



set host "JPADTCRTD01"

set ip "127.0.0.11"

set usuario "LOGIN"

set partida [open "/home/user/Documentos/VALDEMIR/partida.txt"]

set senha [read $partida]


log_user 0



# Habilita log copiando a saída padrão para o arquivo 

log_file -a /home/user/Documentos/SCRIPTS/troughput/tmp/$host ;



# Mágica acontecendo ;p

spawn /usr/bin/ssh $ip -l $usuario


expect {
 "sword:" {
 }
 timeout {
    puts "ERRO. NÃO FOI POSSÍVEL LOGAR NESTE EQUIPAMENTO. LIMITE DE TEMPO EXCEDIDO."	
    exit 1 # para sair dessa parte do script
 }
}



send  "$senha\r"

expect "$host"

send "screen-length 0 temporary\r"

expect "$host"

log_user 3


send "display interface giga 1/0/1 | in rate\r"
expect "$host"

send "display interface giga 1/0/2 | in rate\r"
expect "$host"

send "display interface giga 1/0/3 | in rate\r"
expect "$host"

send "display interface giga 1/0/6 | in rate\r"
expect "$host"

send "display interface giga 1/0/12 | in rate\r"
expect "$host"

send "display interface giga 1/0/13 | in rate\r"
expect "$host"

send "display interface giga 1/0/14 | in rate\r"
expect "$host"

send "display interface giga 1/0/15 | in rate\r"
expect "$host"

send "display interface giga 1/0/16 | in rate\r"
expect "$host"

send "display interface giga 1/0/18 | in rate\r"
expect "$host"

send "display interface giga 2/0/0 | in rate\r"
expect "$host"

send "display interface giga 2/0/1 | in rate\r"
expect "$host"

send "display interface giga 2/0/2 | in rate\r"
expect "$host"

send "display interface giga 2/0/3 | in rate\r"
expect "$host"

send "display interface giga 2/0/8 | in rate\r"
expect "$host"

send "display interface giga 2/0/9 | in rate\r"
expect "$host"

send "display interface giga 2/0/11 | in rate\r"
expect "$host"

send "display interface giga 2/1/1 | in rate\r"
expect "$host"

send "display interface giga 2/1/3 | in rate\r"
expect "$host"

send "display interface giga 3/0/6 | in rate\r"
expect "$host"

send "display interface giga 3/1/5 | in rate\r"
expect "$host"

send "display interface giga 6/0/0 | in rate\r"
expect "$host"

send "display interface giga 6/0/1 | in rate\r"
expect "$host"

send "display interface giga 6/0/2 | in rate\r"
expect "$host"

send "display interface giga 6/0/3 | in rate\r"
expect "$host"

send "display interface giga 6/0/4 | in rate\r"
expect "$host"

send "display interface giga 6/0/5 | in rate\r"
expect "$host"

send "display interface giga 6/0/6 | in rate\r"
expect "$host"

send "display interface giga 6/0/7 | in rate\r"
expect "$host"

send "display interface giga 6/0/8 | in rate\r"
expect "$host"

send "display interface giga 6/0/9 | in rate\r"
expect "$host"

send "display interface giga 6/0/10 | in rate\r"
expect "$host"

send "display interface giga 6/0/11 | in rate\r"
expect "$host"

send "display interface giga 6/1/3 | in rate\r"
expect "$host"

send "display interface giga 6/1/4 | in rate\r"
expect "$host"

send "display interface giga 6/1/5 | in rate\r"
expect "$host"

send "display interface giga 6/1/8 | in rate\r"
expect "$host"

send "display interface giga 6/1/9 | in rate\r"
expect "$host"

send "display interface giga 6/1/10 | in rate\r"
expect "$host"

send "display interface giga 6/1/11 | in rate\r"
expect "$host"

send "display interface giga 7/0/10 | in rate\r"
expect "$host"

send "display interface giga 7/0/12 | in rate\r"
expect "$host"

send "display interface giga 7/0/13 | in rate\r"
expect "$host"

send "display interface giga 7/0/14 | in rate\r"
expect "$host"

send "display interface giga 7/0/15 | in rate\r"
expect "$host"

send "display interface giga 7/0/16 | in rate\r"
expect "$host"

send "display interface giga 7/0/17 | in rate\r"
expect "$host"

send "display interface giga 7/0/18 | in rate\r"
expect "$host"

send "display interface giga 7/0/19 | in rate\r"
expect "$host"

send "display interface giga 7/0/20 | in rate\r"
expect "$host"

send "display interface giga 7/0/21 | in rate\r"
expect "$host"

send "display interface giga 7/0/22 | in rate\r"
expect "$host"

send "display interface giga 7/0/23 | in rate\r"
expect "$host"

send "display interface giga 7/0/24 | in rate\r"
expect "$host"

send "display interface giga 7/0/25 | in rate\r"
expect "$host"

send "display interface giga 7/0/26 | in rate\r"
expect "$host"

send "display interface giga 7/0/27 | in rate\r"
expect "$host"

send "display interface giga 7/0/28 | in rate\r"
expect "$host"

send "display interface giga 7/0/29 | in rate\r"
expect "$host"

send "display interface giga 7/0/30 | in rate\r"
expect "$host"

send "display interface giga 7/0/31 | in rate\r"
expect "$host"

send "display interface giga 7/0/32 | in rate\r"
expect "$host"

send "display interface giga 7/0/33 | in rate\r"
expect "$host"

send "display interface giga 7/0/39 | in rate\r"
expect "$host"

send "display interface giga 8/0/1 | in rate\r"
expect "$host"

send "display interface giga 8/0/2 | in rate\r"
expect "$host"

send "display interface giga 8/0/3 | in rate\r"
expect "$host"

send "display interface giga 8/0/4 | in rate\r"
expect "$host"

send "display interface giga 8/0/6 | in rate\r"
expect "$host"

send "display interface giga 8/0/7 | in rate\r"
expect "$host"

send "display interface giga 8/0/8 | in rate\r"
expect "$host"

send "display interface giga 8/0/9 | in rate\r"
expect "$host"

send "display interface giga 8/0/10 | in rate\r"
expect "$host"

send "display interface giga 8/0/11 | in rate\r"
expect "$host"

send "display interface giga 8/0/12 | in rate\r"
expect "$host"

send "display interface giga 8/0/13 | in rate\r"
expect "$host"

send "display interface giga 8/0/14 | in rate\r"
expect "$host"

send "display interface giga 8/0/18 | in rate\r"
expect "$host"

send "display interface giga 8/0/19 | in rate\r"
expect "$host"

send "display interface giga 8/0/22 | in rate\r"
expect "$host"

send "display interface giga 8/0/25 | in rate\r"
expect "$host"

send "display interface giga 8/0/31 | in rate\r"
expect "$host"

send "display interface giga 8/0/34 | in rate\r"
expect "$host"

send "display interface giga 8/0/35 | in rate\r"
expect "$host"

send "display interface giga 8/0/37 | in rate\r"
expect "$host"

send "display interface giga 8/0/38 | in rate\r"
expect "$host"

send "display interface giga 8/0/39 | in rate\r"
expect "$host"



send "quit\r"

expect eof

close $partida

log_file ; #para o log desse arquivo




