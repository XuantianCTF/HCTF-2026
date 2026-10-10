CC      = gcc
CFLAGS  = -O0 -no-pie -fno-stack-protector -Wall
CLIENT  = client.elf
SERVER  = server.elf

.PHONY: all clean

all: $(CLIENT) $(SERVER)

$(CLIENT): client.c proto.c proto.h
	$(CC) $(CFLAGS) -o $(CLIENT) client.c proto.c

$(SERVER): server.c proto.c proto.h
	$(CC) $(CFLAGS) -o $(SERVER) server.c proto.c

clean:
	rm -f $(CLIENT) $(SERVER)
