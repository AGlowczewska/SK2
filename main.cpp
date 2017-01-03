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
pthread_mutex_t myMutex = PTHREAD_MUTEX_INITIALIZER;
int Clients = 0; // number of connected clients

 struct Thread{
    int Id;
    string Name;
};

Thread THREADS[QUEUE_SIZE]; // list of threads

/*Function for reading from the socket */
void *reading(void *client){

}

/*Function for sending list of currently connected clients to server */
void update(){

}

/* Function for connecting clients to server */
void connect(int mySocket){
    int myConnection;
    char myBuffer[BUF_SIZE];

    myConnection = accept(mySocket,NULL, NULL);
    struct Thread data;
    data.Id = myConnection;
    if (myConnection < 0) {
        cerr << "ERROR: Can't create connection socket." << endl;
        exit(1);
    } else {
        cout << "Connection socket created:" << myConnection << endl;
        bzero(myBuffer, BUF_SIZE);
        read(myConnection, myBuffer, BUF_SIZE);
        data.Name = myBuffer;
        cout << "Client login:" << data.Name << endl;
    }

    pthread_t client;
    if (pthread_create(&client, NULL, reading, (void *)&data) == 1){
        cerr << "ERROR: Creating thread" << endl;
        exit(1);
    } else {
        pthread_mutex_lock(&myMutex);
        for (int i=0; i < QUEUE_SIZE; i++)
            if (THREADS[i].Id == 0) {
                THREADS[i].Id = data.Id;
                THREADS[i].Name = data.Name;
                cout << "Przypisano do id:" << i << endl;
                break;
            }
        Clients++;
        pthread_mutex_unlock(&myMutex);
        cout << "Number of current connections:" << Clients << endl;
    }

    //update()
}

int main(int argc, char *argv[]){

    /** Initializing the THREADS table **/
    for (int i=0; i < QUEUE_SIZE; i++){
        THREADS[i].Id = 0;
        THREADS[i].Name = ' ';
    };
    /************************************/


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
    cout << "Waiting for clients to join..." <<endl;

    while(1){
        if (Clients < 5) connect(mySocket);
    }

    return 0;
}