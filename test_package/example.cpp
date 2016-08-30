#include <node.h>

int main()
{
  char *argv[] = {"example", "-v", NULL};
  int argc = sizeof(argv) / sizeof(char*) - 1;
  return node::Start(argc, argv);
}
