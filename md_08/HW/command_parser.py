from argparse import Namespace, ArgumentParser

class MyArgumentParser(ArgumentParser):
    def exit(self, status=0, message=None):
        if status:
            pass

parser = MyArgumentParser(usage='command{name, tag, tags}: argument(s)', exit_on_error=False)
# subparsers = parser.add_subparsers(dest='command')

parser.add_argument('command', type=str, default='No command')
parser.add_argument('arguments', type=str, nargs='+', default='No arguments')

# name_parser = subparsers.add_parser('name:')
# name_parser.add_argument('arguments', type=str)

# tag_parser = subparsers.add_parser('tag:')
# tag_parser.add_argument('arguments', type=str)

# tags_parser = subparsers.add_parser('tags:')
# tags_parser.add_argument('arguments', type=str, nargs='+')


def parse_args(input: str) -> dict[str, str]|None:
    '''Parse the command line arguments
    :param input: input string
    :return: dictionary which contains command and arguments key:value pair
    In order to be able to cache further functions results parsed arguments don't
    have to be split into list'''
    if not input:
        print('Please enter a query command or exit to end program')        
        return None
    if input.count(':') != 1:
        print("Command string from arguments must be devided by colon ':' and there should be only one.")        
        return None
    
    parsed_input = input.split(':')
    command = parsed_input[0].strip()
    arguments = parsed_input[1].strip()
    return {'command': command, 'arguments': arguments}
     


# def parse_args(input: str) -> dict[str, list[str]]:
#     '''Parse the input strin arguments
#     :param input: input string
#     :return: Namespace object'''
    # stack = []
    # result = []
    # for el in input.split():
    #     if el.startswith('"'):
    #         stack.append(el)
    #         continue
    #     elif el.endswith('"'):
    #         if len(stack) >= 1:
    #             new_el = stack.pop() + ' ' + el
    #             result.append(new_el.strip('"'))
    #             continue
    #     result.append(el)

    # args = parser.parse_args(input)
    # args_dict = vars(args)
    # return args_dict


if __name__ == '__main__':
    pass
    args = parse_args('name: "Alber Einstein"')
    print(vars(args))