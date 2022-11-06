#include <stdio.h>
#include <string.h>
#include <arpa/inet.h>
#include <openssl/sha.h>

unsigned char *additionalMsg = "&download=secret.txt";

// The MAC for the valid URL
int a[8] = {  0x3912fe08, 0x949c7c09, 0xbd2825b0, 0x1a2e8e9c,
              0x151d84be, 0x0106e858, 0x4e9006b8, 0x8a22555f };


int main(int argc, const char *argv[])
{
  int i;
  unsigned char buffer[SHA256_DIGEST_LENGTH];
  SHA256_CTX c;

  SHA256_Init(&c);

  /* We assume that the padded original message has 64 bytes (i.e., 1 block).
   * If that is not true, modify 64 accordingly, e.g. use 128 for 2 blocks. 
   * This step is important, because that is how we tell the hash function
   * the length of our message. */
  for (i=0; i<64; i++)  SHA256_Update(&c, "*", 1);

  for (i=0; i<8; i++)   c.h[i] = htole32(a[i]);

  // Append the additional message
  SHA256_Update(&c, additionalMsg, strlen(additionalMsg));
  SHA256_Final(buffer, &c);
  for (i = 0; i < 32; i++) {
      printf("%02x", buffer[i]);
  }
  printf("\n");

  return 0;
}
