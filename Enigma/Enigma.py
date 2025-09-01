"""
00 1054560
01 342732000
02 47297016000
03 3641870232000
04 172988836020000
05 5293458382212000
06 105869167644240000
07 1376299179375120000
08 11354468229844740000
09 56772341149223700000
10 158962555217826360000
11 216767120751581400000
12 108383560375790700000
13 8337196951983900000

from math import factorial
def f(k: int):
    return 60 * 26 ** 3 * factorial(26) // (factorial(26 - 2 * k) * factorial(k) * 2 ** k)
def g(k: int):
    return 26 ** 2 * factorial(26) ** 5 // (2 ** (13 + k) * factorial(13) * factorial(26 - 2 * k) * factorial(k))
print(f(10), f(11), sum(map(f, range(14))), g(10), g(11), sum(map(g, range(14))), sep='\n')

                 f(10) =  158962555217826360000
                 f(11) =  216767120751581400000
sum(map(f, range(14))) =  562064881159999426560
                 g(10) =  52841615182541934867380880379974902806941642035152636578099608189263918507485623746560000000000000000000000000
                 g(11) =  72056747976193547546428473245420322009465875502480868061044920258087161601116759654400000000000000000000000000
sum(map(g, range(14))) = 186839071108157384996636441415047152219471994297031498823429747361328478992481746954485760000000000000000000000

usgovernmentofficialshavedisputedcriticismsofprismintheguardianandwashingtonpostarticlesandhavedefendedtheprogramassertingthatitcannotbeusedondomestictargetswithoutawarrantthatithashelpedtopreventactsofterrorismandthatitreceivesindependentoversightfromthefederalgovernmentsexecutivejudicialandlegislativebranches
dttnjmhxnjyqfovbienfpjwbmsxicrqbzbcochlvrvukwfshbbogbbwclgpojxhhqgmjoggllkekkfdzznvbyghflwvxgwijmedtsfijntkauvemjxadgnvmoixefkuetsqgfhpxezuslzyryvvbhlrdhdhvuvnujrgyhrylwqtkayqnmbxqrctuvceerebbbrfobhoxtsomhxdgbjfpcpfptybdnimvjotllchpidmiqhgnjgnoqhixsbprhwzdlvbaodfvnazyvtljkxtppiwenrwderwwzrkdwpccucuiwtdblbtcxomp

zgfyjkjigdgdakyscwyckdcknx

veczyptmon
decryption
"""

_all__ = ["Pair", "Rotor", "all_rotors", "reflector", "civil_encryption", "military_encryption"]


class Pair:
    def __init__(self, fst: str, snd: str):
        if fst == snd or (len(fst), len(snd)) != (1, 1):
            raise ValueError
        self.first, self.second = fst, snd

    def other(self, _l):
        if _l in {self.first, self.second}:
            return [self.first, self.second][_l == self.first]

        raise KeyError("Unrecognized symbol")

    def __contains__(self, item):
        return item in {self.first, self.second}

    def __eq__(self, other):
        return self.first in other and self.second in other

    def __str__(self):
        return self.first + '-' + self.second

    __repr__ = __str__


class Rotor:
    def __init__(self, value: str):
        if len(value) != 26:
            raise ValueError
        self.__rotor = value

    @property
    def rotor(self):
        return self.__rotor

    def copy(self):
        return Rotor(self.rotor)

    def index(self, c: str):
        return self.__rotor.index(c)

    def rotated(self):
        return Rotor(self.rotor[1:] + self.rotor[0])

    def __len__(self):
        return 26

    def __getitem__(self, item):
        return self.rotor[item]

    def __eq__(self, other):
        if not isinstance(other, Rotor) or len(self) != len(other):
            return False
        this_value = list(self.rotor)
        other_value = list(other.rotor)
        for _ in range(len(self)):
            if this_value == other_value:
                return True
            this_value = this_value[1:] + [this_value[0]]
        return False

    def __str__(self):
        return ' '.join(self.rotor)

    __repr__ = __str__


rotor1 = Rotor('vytabhdqojlsuepfriwcxngmkz')
rotor2 = Rotor('fwoiphmxknurscqeaglvdbtjzy')
rotor3 = Rotor('vknhdfbulcqprjzemogxitsayw')
rotor4 = Rotor('xtkazsnyolwqifugdpbrmjchev')
rotor5 = Rotor('lmeoipfgysbrkhjudqcvanxwzt')
all_rotors = [rotor1, rotor2, rotor3, rotor4, rotor5]
reflector = [Pair('a', 'p'), Pair('h', 'l'), Pair('v', 'n'), Pair('s', 'z'), Pair('k', 'x'), Pair('e', 'b'),
             Pair('q', 'w'), Pair('j', 'm'), Pair('i', 'd'), Pair('o', 'c'), Pair('u', 'g'), Pair('t', 'f'),
             Pair('r', 'y')]


def civil_encryption(message: str, rotors: list[Rotor], rotor1rotations: int, rotor2rotations: int,
                     rotor3rotations: int) -> str:
    for _ in range(rotor1rotations):
        rotors[0] = rotors[0].rotated()

    for _ in range(rotor2rotations):
        rotors[1] = rotors[1].rotated()

    for _ in range(rotor3rotations):
        rotors[2] = rotors[2].rotated()

    res, total = '', rotor1rotations % 26

    for l in message.lower():
        if l.isalpha():
            total += 1
            rotors[0] = rotors[0].rotated()

            if not total % 26:
                rotors[1] = rotors[1].rotated()

                if not total % 676:
                    rotors[2] = rotors[2].rotated()

            l = rotors[0][ord(l) - 97]
            l = rotors[1][ord(l) - 97]
            l = rotors[2][ord(l) - 97]

            for p in reflector:
                if l in p:
                    l = p.other(l)

                    break

            l = chr(rotors[2].index(l) + 97)
            l = chr(rotors[1].index(l) + 97)
            l = chr(rotors[0].index(l) + 97)

        res += l

    return res


plugboard = [Pair('n', 'e'), Pair('l', 't'), Pair('y', 's'), Pair('d', 'v'), Pair('q', 'h'),
             Pair('p', 'c'), Pair('k', 'o'), Pair('r', 'm'), Pair('u', 'i'), Pair('g', 'f')]


def military_encryption(message: str, rotors: list[Rotor], rotor1rotations: int, rotor2rotations: int,
                        rotor3rotations: int, _plugboard: list[Pair]) -> str:
    res = list(civil_encryption(message, rotors, rotor1rotations, rotor2rotations, rotor3rotations))

    for i, l in enumerate(res):
        for p in _plugboard:
            if l in p:
                res[i] = p.other(l)

                break

    return ''.join(res)


if __name__ == "__main__":
    print(civil_encryption('testingencryptiondecryption', [rotor1, rotor2, rotor3], 2, 1, 1))
