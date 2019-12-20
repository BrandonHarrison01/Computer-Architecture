"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001

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
            MUL: self.mul,
            ADD: self.add,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call,
            RET: self.ret
        }
        self.halted = False
        self.stack_pointer = 7
        self.reg[self.stack_pointer] = 0b11110100



    def load(self):
        """Load a program into memory."""
        
        filename = sys.argv[1]
        address = 0

        with open(filename) as f:
            for line in f:
                n = line.split('#')
                n[0] = n[0].strip()

                if n[0] == '':
                    continue

                val = int(n[0], 2)
                self.ram[address] = val
                # print(program, val)
                address += 1


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
        op1 = self.ram[self.__pc + 1]
        op2 = self.ram[self.__pc + 2]
        self.alu('MUL', op1, op2)
        
        self.__pc += 3


    def add(self):
        op1 = self.ram[self.__pc + 1]
        op2 = self.ram[self.__pc + 2]
        self.alu('ADD', op1, op2)
        
        self.__pc += 3


    def hlt(self):
        self.halted = True


    def push(self):
        print(self.reg[self.stack_pointer], 'pre dec')
        self.reg[self.stack_pointer] -= 1 # <-- decrementing value stored in register 7
        print(self.reg[self.stack_pointer], 'post dec')

        register_num = self.ram[self.__pc + 1] # <-- getting register number from next instruction
        value = self.reg[register_num]  # <-- setting a variable called value to the value found in register with given register number
        self.ram[self.reg[self.stack_pointer]] = value # <-- ?? putting value in the stack at the value being stored in reg[7]

        self.__pc += 2


    def pop(self):
        register_num = self.ram[self.__pc + 1]
        value = self.ram[self.reg[self.stack_pointer]]
        self.reg[register_num] = value

        self.reg[self.stack_pointer] += 1
        self.__pc += 2


    def call(self):
        push_val = self.__pc + 2  # <-- setting value push_val to next instruction
        self.reg[self.stack_pointer] -= 1  # <-- decrementing value in reg[7]
        self.ram[self.reg[self.stack_pointer]] = push_val  # <-- setting value of ram at reg[7]'s value to the next instrucion
        # print(self.__pc, 'call')
        self.__pc = self.reg[self.ram[self.__pc + 1]]  # <-- moving program counter to value stored in given register


    def ret(self):
        pop_val = self.ram[self.reg[self.stack_pointer]]  # <-- setting variable ret_add to value found at ram index stored in reg[7]
        self.reg[self.stack_pointer] += 1  # <-- incrementing value stored in reg[7]
        self.__pc = pop_val  # <-- moving program counter to ret_add
        # print(self.__pc)


    def run(self):
        """Run the CPU."""

        while not self.halted:
            instruction = self.ram[self.__pc]

            self.branchtable[instruction]()

