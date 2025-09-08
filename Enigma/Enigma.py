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


rotor0 = Rotor('vytabhdqojlsuepfriwcxngmkz')
rotor1 = Rotor('fwoiphmxknurscqeaglvdbtjzy')
rotor2 = Rotor('vknhdfbulcqprjzemogxitsayw')
rotor3 = Rotor('xtkazsnyolwqifugdpbrmjchev')
rotor4 = Rotor('lmeoipfgysbrkhjudqcvanxwzt')
all_rotors = [rotor0, rotor1, rotor2, rotor3, rotor4]
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
    print(civil_encryption('testingencryptiondecryption', [rotor0, rotor1, rotor2], 2, 1, 1))
