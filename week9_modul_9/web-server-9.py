from socket import * #mengimport semua library socket

serverPort = 3758    #memilih port bebas untuk server
serverSocket = socket(AF_INET, SOCK_STREAM) #menggunakan TCP sebagai protokolnya
serverSocket.bind(('', serverPort))  #mengikat socket ke port yang telah dipilih

serverSocket.listen(3)               #server terima konseksi dengan antrian maks 3
print('Server siap menerima koneksi client...') #print kalimat disamping

while True: #perulangan untuk terus menerima koneksi dari client
    connectionSocket, addr = serverSocket.accept() #terima konseksi dari client dengan address client
    print('Siap melayani address... ', addr)       #print kalimat disamping dengan address client

    try:  #try untuk menerima pesan dari client dan memprosesnya
        message= connectionSocket.recv(2048).decode() #terima pesan dgn ukuran 2048 byte dan masukkan ke variable message
        print('pesan diterima: ', message)            #print kalimat pesan diterima dengan isi pesan

        #ini yang disuruh lengkapi dari modul 9
        filename = message.split()[1] #memisahkan pesan dengan spasi dan mengambil bagian kedua sebagai nama file
        f = open(filename[1:])        #hapus karakter "/" pada pesan dan buka file dengan nama tersebut
        
        outputdata = f.read()         #baca file dan simpan pada variable outputdata  
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode()) #kirim response header HTTP 200 OK ke client
        
        #ini yang disuruh lengkapi dari modul 9
        for i in range(0, len(outputdata)):   #perulangan untuk kirim data pecahan HTML ke client
            connectionSocket.send(outputdata[i].encode()) #kirim data pecahan HTML ke client dengan encode

        connectionSocket.send("\r\n".encode()) #kirim karakter baru untuk menandai akhir dari response 
        connectionSocket.close()               #tutup koneksi dengan client

    except:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode()) #digunakan untuk kirim status header 404 error
        connectionSocket.send("Content-Type: text/html\r\n".encode()) #beritahu browser bahwa yang dikirim HTML
        connectionSocket.send("\r\n".encode())                   #tandai bahawa response dari server udah selesai
        connectionSocket.send("<h1>404 Not Found</h1>".encode()) #kirim Body HTML 404 not found
    connectionSocket.close()#diluar whle, tutup koneksi dengan client