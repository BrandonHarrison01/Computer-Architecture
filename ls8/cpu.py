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
        self.branchtable = {
            LDI: self.ldi,
            PRN: self.prn,
            HLT: self.hlt,
            MUL: self.mul
        }
        self.halted = False



    def load(self):
        """Load a program into memory."""

        program = [0] * 256
        
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
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b] 
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


    def ldi(self):
        register_num = self.ram[self.__pc + 1]
        self.reg[register_num] = self.ram[self.__pc + 2]
        self.__pc += 3


    def prn(self):
        index = self.ram[self.__pc + 1]
        register_num = self.reg[index]
        print(register_num)
        self.__pc += 2


    def mul(self):
        self.alu('MUL', 0, 1)
        self.__pc += 3
        

    def hlt(self):
        self.halted = True


    def run(self):
        """Run the CPU."""

        while not self.halted:
            instruction = self.ram[self.__pc]

            self.branchtable[instruction]()

