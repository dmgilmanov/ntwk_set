import netmiko, getpass, sys, socket, telnetlib, time, re
from netmiko import ConnectHandler

print(time.strftime("%d-%m-%Y"))
username = input("Введите имя пользователя: ")
password = getpass.getpass()
port = 22

#Read IP address information.
with open ('ip_add.txt') as	file:
	ip = [row.strip() for row in file]

#Open output.txt file for loging.
ouput_file = open ('ouput.txt', 'w')

#Open errors.txt file for error loging.
ouput_file_errors = open ('errors.txt', 'w')

#SSH connecting function
def SSH_CONNECT (ip_in):
	
	#Параметры подключения
	juniper = {
		'device_type': 'juniper',
		'ip': ip_in,
		'username': username,
		'password': password,
		'port': 22,
	}
	
	#Подключение к устройству
	connect_ssh = ConnectHandler(**juniper)
	
	#Выполнение команд из файла input.txt
	output = connect_ssh.send_config_from_file('config.txt')
	
	print (output)
	ouput_file.write (output)
	
	#Закрытие подключение
	connect_ssh.disconnect()

#Счетчик ошибок
e = 0
	
#Основной цикл. Перебор всех IP из файла ip.txt
i = 0
while i < len(ip):
	
	#Печать заголовка в консоль и файл ouput.txt
	print ('\n\n' + '----------------------' + '\n' + ip[i] + ' (' + str(i+1) + '/' + str(len(ip)) + ')\n' + '----------------------')
	ouput_file.write ('\n' + '---------------' + '\n' + ip[i] + '\n' + '---------------')
	
	try:
		SSH_CONNECT (ip[i])
	except BaseException:
		print ('Ошибка модуля SSH')
		ouput_file.write ('\n' + 'Ошибка модуля SSH' + '\n')
		ouput_file_errors.write (ip[i] + '\n')
		e = e + 1
				
	i = i + 1

#Опрошено устройств
print ('\n\n' + '----------------------' + '\n' + 'Обработано устройств: ' + str(i) + '\n')
ouput_file.write ('\n' + '----------------------' + '\n' + 'Обработано устройств: ' + str(i) + '\n')

#Количество ошибок
print ('Количество ошибок: ' + str(e))
ouput_file.write ('Количество ошибок: ' + str(e))

#Закрываем файлы для вывода
ouput_file.close
ouput_file_errors.close
	
