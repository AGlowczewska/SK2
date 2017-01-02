
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <signal.h>
#include <pthread.h>
#include <iostream>

#define BUF_SIZE 256
#define SERVER_PORT 2056
#define QUEUE_SIZE 5

using namespace std;

int THREADS[5];
int ThreadNumber = 0;

/* struct thread_data_t{
    int myNumber;
    int descriptor;
}; */

int main(int argc, char *argv[]){
    struct sockaddr_in myServer;
    memset(&myServer, 0, sizeof(struct sockaddr));
    myServer.sin_family = AF_INET;
    myServer.sin_addr.s_addr = htonl(INADDR_ANY);
    myServer.sin_port = htons(SERVER_PORT);

    int mySocket = socket(AF_INET, SOCK_STREAM, 0);
    if(mySocket < 0){
        cerr << "ERROR: Socket creating" << endl;
        exit(1);
    }

    char temp = 1;
    setsockopt(mySocket, SOL_SOCKET, SO_REUSEADDR, (char*)&temp, sizeof(temp));
   cout << "Socket created" << endl;

    int myBind = bind(mySocket, (struct sockaddr*)&myServer, sizeof(struct sockaddr));
    if(myBind < 0 ){
        cerr << "ERROR: Binding IP and port to socket" << endl;
        exit(1);
    }
   cout << "Socket binded..." << endl;

    int myListen = listen(mySocket, QUEUE_SIZE);
    if (myListen < 0 ){
        cerr << "ERROR: Queque size"<< endl;
        exit(1);
    }

    int myConnection;

    char myBuffer[BUF_SIZE];
    bzero(myBuffer, BUF_SIZE);
    cout << "Waiting for client..." <<endl;
    while(1){
        myConnection = accept(mySocket,NULL, NULL);
        if (myConnection < 0) {
            cerr << "ERROR: Can't create connection socket." << endl;
            exit(1);
        }
        write(myConnection, myBuffer, sizeof(myBuffer));
        cout << "Deskryptor połączenia:" << myConnection << endl;
        cout << "Connection socket created... " << endl;
        break;
    }

    return 0;
}