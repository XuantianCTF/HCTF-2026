package main

import (
	"bufio"
	"fmt"
	"os"
)

var secret = []byte{
	0x2f, 0x2c, 0x24, 0x2e, 0x1e, 0x15, 0x57, 0x03, 0x11, 0x06, 0x02,
	0x2d, 0x1f, 0x5f, 0x02, 0x37, 0x54, 0x01, 0x38, 0x0a, 0x0a, 0x15,
}

var key = "gopher"

func check(flag string) bool {
	if len(flag) != len(secret) {
		return false
	}
	for i := 0; i < len(secret); i++ {
		if flag[i]^key[i%len(key)] != secret[i] {
			return false
		}
	}
	return true
}

func main() {
	fmt.Println("==========================================")
	fmt.Println("            HCTF 2026 | ezgo")
	fmt.Println("==========================================")
	fmt.Print("Please input the flag: ")

	scanner := bufio.NewScanner(os.Stdin)
	if !scanner.Scan() {
		return
	}

	if check(scanner.Text()) {
		fmt.Println("Correct! You are a Go reverser now :)")
	} else {
		fmt.Println("Wrong! Keep trying :(")
	}
}
