from time import time

from itertools import permutations

from Enigma import *

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def decrypt_civil_enigma(message: str, supposed_substring: str):
    for i in range(len(message) - len(supposed_substring) + 1):
        if all(supposed_substring[_] != message[i + _] for _ in range(len(supposed_substring))):
            for rotors in map(list, permutations(all_rotors, 3)):
                for rotor3rotations in range(26):
                    curr_rotor_2 = rotors[2].copy()

                    for rotor2rotations in range(26):
                        curr_rotor_1 = rotors[1].copy()

                        for rotor1rotations in range(26):
                            curr_rotor_0 = rotors[0].copy()

                            for _ in range(i):
                                curr_rotor_0 = curr_rotor_0.rotated()

                                if not (_ + 1) % 26:
                                    curr_rotor_1 = curr_rotor_1.rotated()

                                    if not (_ + 1) % 676:
                                        curr_rotor_2 = curr_rotor_2.rotated()

                            total, works = i, True

                            for j, l in enumerate(supposed_substring):
                                total += 1
                                curr_rotor_0 = curr_rotor_0.rotated()

                                if not total % 26:
                                    curr_rotor_1 = curr_rotor_1.rotated()

                                    if not total % 676:
                                        curr_rotor_2 = curr_rotor_2.rotated()

                                l = curr_rotor_0[ord(l) - 97]
                                l = curr_rotor_1[ord(l) - 97]
                                l = curr_rotor_2[ord(l) - 97]

                                for p in reflector:
                                    if l in p:
                                        l = p.other(l)

                                        break

                                l = chr(curr_rotor_2.index(l) + 97)
                                l = chr(curr_rotor_1.index(l) + 97)
                                l = chr(curr_rotor_0.index(l) + 97)

                                if l != message[i + j]:
                                    works = False

                                    break

                            if works:
                                yield f'{all_rotors.index(rotors[0]) + 1} {all_rotors.index(rotors[1]) + 1} {all_rotors.index(rotors[2]) + 1} | {rotor1rotations:02d} {rotor2rotations:02d} {rotor3rotations:02d} -> {civil_encryption(message, rotors.copy(), 0, 0, 0)}'

                            rotors[0] = rotors[0].rotated()

                        rotors[1] = rotors[1].rotated()

                    rotors[2] = rotors[2].rotated()


def decrypt_military_enigma(message: str, supposed_substring: str):
    def work_out_plugboard(current_substring: str, rotor0, rotor1, rotor2, total: int, pairs=None, curr_pairs=None,
                           singles=None, poison_tree=None):
        def free(letter: str):
            for pair in pairs:
                if letter in pair:
                    return False

            return letter not in singles

        if not current_substring:
            yield f"{all_rotors.index(rotors[0]) + 1} {all_rotors.index(rotors[1]) + 1} {all_rotors.index(rotors[2]) + 1} | {rotor1rotations:02d} {rotor2rotations:02d} {rotor3rotations:02d} | {pairs} | {''.join(filter(free, ALPHABET))}" + ' ' * (
                not singles) + f"-> {military_encryption(message, rotors.copy(), 0, 0, 0, pairs)}"
            return
        if poison_tree is None:
            poison_tree = []

        if singles is None:
            singles = set()

        if curr_pairs is None:
            curr_pairs = []

        if pairs is None:
            pairs = []

        if len(pairs) == 10:
            singles.update({l for l in ALPHABET if free(l)})

        if free(current_substring[0]):
            for other in ALPHABET.replace(current_substring[0], ' '):
                _pairs, _singles = pairs.copy(), singles.copy()

                if other == ' ':
                    _singles.add(current_substring[0])
                else:
                    if not free(other) or Pair(current_substring[0], other) in poison_tree:
                        continue

                    _pairs.append(Pair(current_substring[0], other))

                for _res in work_out_plugboard(current_substring, rotor0, rotor1, rotor2, total, _pairs,
                                               [Pair(current_substring[0], other)], _singles):
                    yield _res

            return

        _rotor0, _rotor1, _rotor2 = rotor0.copy(), rotor1.copy(), rotor2.copy()
        _rotor0 = _rotor0.rotated()

        if not (total + 1) % 26:
            _rotor1 = _rotor1.rotated()

            if not (total + 1) % 676:
                _rotor2 = _rotor2.rotated()

        l = current_substring[0]

        for p in pairs:
            if l in p:
                l = p.other(l)

                break

        l = _rotor0[ord(l) - 97]
        l = _rotor1[ord(l) - 97]
        l = _rotor2[ord(l) - 97]

        for p in reflector:
            if l in p:
                l = p.other(l)

                break

        l = chr(_rotor2.index(l) + 97)
        l = chr(_rotor1.index(l) + 97)
        l = chr(_rotor0.index(l) + 97)
        works = True

        if l != message[i + total]:
            if Pair(l, message[i + total]) not in pairs:
                if len(pairs) == 10 or Pair(l, message[i + total]) in poison_tree or not (
                        free(l) and free(message[i + total])):
                    works = False
                    poison_tree += [_p for _p in curr_pairs + [Pair(l, message[i + total])] if _p not in poison_tree]
                else:
                    pairs.append(Pair(l, message[i + total])), curr_pairs.append(Pair(l, message[i + total]))

                    if len(pairs) == 10:
                        singles.update({l for l in ALPHABET if free(l)})
        elif len(singles) == 6 or any(Pair(l, _) in pairs for _ in ALPHABET.replace(l, '')):
            works = False
            poison_tree += list(filter(lambda _p: _p not in poison_tree, curr_pairs))
        else:
            singles.add(l)

        if len(poison_tree) > 315:
            raise ValueError

        if not works:
            return

        for _res in work_out_plugboard(current_substring[1:], _rotor0, _rotor1, _rotor2, total + 1, pairs, curr_pairs,
                                       singles, poison_tree):
            yield _res

    for i in range(len(message) - len(supposed_substring) + 1):
        if all(supposed_substring[_] != message[i + _] for _ in range(len(supposed_substring))):
            for rotors in map(list, permutations(all_rotors, 3)):
                for rotor3rotations in range(26):
                    curr_rotor_2 = rotors[2].copy()

                    for rotor2rotations in range(26):
                        curr_rotor_1 = rotors[1].copy()

                        for rotor1rotations in range(26):
                            curr_rotor_0 = rotors[0].copy()

                            for _ in range(i):
                                curr_rotor_0 = curr_rotor_0.rotated()

                                if not (_ + 1) % 26:
                                    curr_rotor_1 = curr_rotor_1.rotated()
                                    if not (_ + 1) % 676:
                                        curr_rotor_2 = curr_rotor_2.rotated()
                            try:
                                for res in work_out_plugboard(supposed_substring, curr_rotor_0.copy(),
                                                              curr_rotor_1.copy(), curr_rotor_2.copy(), i):
                                    yield res
                            except ValueError:
                                ...

                            rotors[0] = rotors[0].rotated()

                        rotors[1] = rotors[1].rotated()

                    rotors[2] = rotors[2].rotated()


item = decrypt_civil_enigma('nfiyzlxawymgksnxwtjlnslnndc', 'testinge')
# 1 2 3 | 02 01 01 | [t-l, h-q, e-n, s-y, f-g] | bcdijkmopruvwxz-> testuwg 31.431917190551758
t = time()

for el in item:
    print(el, time() - t)
# 1 2 3 | 01 01 02 | [t-l, e-n, s-y, i-u, g-f, k-o, r-m, c-p, q-h] | adjv-> testingencryptionveczyptmon 622.9634838104248
# 1 2 3 | 02 01 01 | [t-l, h-q, e-n, s-y, f-g, i-u, m-r, d-v, c-p, o-k] | -> testingencryptiondecrypioon 42.60205960273743
