#include "code.h"

void main()
{
    char buff_group_name[255];
    welcome_message();
    get_name(buff_group_name);
    create_folder("data");
    create_file("data", buff_group_name);
}