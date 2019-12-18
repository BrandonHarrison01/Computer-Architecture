"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = {}
        self.reg = [0] * 8
        self.__pc = 0

    def load(self):
        """Load a program into memory."""

        # For now, we've just hardcoded a program:

        program = [0] * 256
            # # From print8.ls8
            # 0b10000010, # LDI R0,8
            # 0b00000000,
            # 0b00001000,
            # 0b01000111, # PRN R0
            # 0b00000000,
            # 0b00000001, # HLT
        

        filename = sys.argv[1]
        address = 0

        with open(filename) as f:
            for line in f:
                n = line.split('#')
                n[0] = n[0].strip()

                if n[0] == '':
                    continue

                val = int(n[0], 2)
                program[address] = val
                # print(program, val)
                address += 1

        print(program[:20])
        # sys.exit()

        index = 0

        for instruction in program:
            self.ram[index] = instruction
            index += 1

        # print('test 2')


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # print(self.ram, 'test')
        halted = False
        while not halted:
            instruction = self.ram[self.__pc]

            if instruction == HLT:
                halted = True

            elif instruction == LDI:
                register_num = self.ram[self.__pc + 1]
                self.reg[register_num] = self.ram[self.__pc + 2]
                self.__pc += 3
            
            elif instruction == PRN:
                index = self.ram[self.__pc + 1]
                register_num = self.reg[index]
                print(register_num)
                self.__pc += 2

            elif instruction == MUL:
                print(self.ram[self.__pc + 1] * self.ram[self.__pc + 2])
                self.__pc += 3

            else:
                print(f'problem at {self.__pc}')
