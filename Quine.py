class Quine:
    def __init__(self, minterms: list, dont_care: list):
        self.__minterms = minterms
        self.__dont_care = dont_care
        self.__minterms_with_dont_care = minterms + dont_care

    def __mul(self, x, y):
        """
        Multiply 2 minterms
        """
        result = []
        for i in x:
            if i + "'" in y or (len(i) == 2 and i[0] in y):
                return []
            else:
                result.append(i)
        for i in y:
            if i not in result:
                result.append(i)
        return result

    def __multiply(self, x, y):
        """
        Multiply 2 expressions
        """
        result = []
        for i in x:
            for j in y:
                temp = self.__mul(i, j)
                result.append(temp) if len(temp) != 0 else None
        return result

    def __refine(self, my_list, dc_list):
        """
        Xoa cac don't care khoi danh dach va tra ve danh sach da xoa
        """
        result = []
        for i in my_list:
            if int(i) not in dc_list:
                result.append(i)
        return result

    def __findEPI(self, x):
        """
        Tim cac essential prime implicants tu cac prime implicants
        """
        result = []
        for i in x:
            if len(x[i]) == 1:
                result.append(x[i][0]) if x[i][0] not in result else None
        return result

    def __find_variables(self, x):
        """
        Tim bien bieu dien boi cac minterms.\n
        Vi du, minterm --01 duoc bieu dien boi C' va D
        """
        var_list = []
        for i in range(len(x)):
            if x[i] == '0':
                var_list.append(chr(i + 65) + "'")
            elif x[i] == '1':
                var_list.append(chr(i + 65))
        return var_list

    def __flatten(self, x):
        """
        Chuyen dict thanh list 
        """
        flattened_items = []
        for i in x:
            flattened_items.extend(x[i])
        return flattened_items

    def __find_minterms(self, a):
        """
        Tim ra cac mintern bi thay the boi ki tu "-".\n
        Vi du, 10-1 la 9(1001) va 11(1011)
        """
        gaps = a.count('-')
        if gaps == 0:
            return [str(int(a, 2))]
        x = [bin(i)[2:].zfill(gaps) for i in range(pow(2, gaps))]
        temp = []
        for i in range(pow(2, gaps)):
            temp2, ind = a[:], -1
            for j in x[0]:
                if ind != -1:
                    ind = ind + temp2[ind + 1:].find('-') + 1
                else:
                    ind = temp2[ind + 1:].find('-')
                temp2 = temp2[:ind] + j + temp2[ind + 1:]
            temp.append(str(int(temp2, 2)))
            x.pop(0)
        return temp

    def __compare(self, a, b):
        """
        Kiem tra xem 2 minterm khac nhau 1 bit hay khong \n
        Tra ve True, False va vi tri khac nhau
        """
        mismatch_index = 0
        c = 0
        for i in range(len(a)):
            if a[i] != b[i]:
                mismatch_index = i
                c += 1
                if c > 1:
                    return False, None
        return True, mismatch_index

    def __remove_terms(self, _chart, terms):
        """
        Removes minterms which are already covered from chart
        """
        for i in terms:
            for j in self.__find_minterms(i):
                try:
                    del _chart[j]
                except KeyError:
                    pass

    def __group_primary(self, minterms, size):
        """
        Nhom cac minterm theo so chu so 1
        """
        groups = {}
        for minterm in minterms:
            try:
                groups[bin(minterm).count('1')].append(
                    bin(minterm)[2:].zfill(size))
            except KeyError:
                groups[bin(minterm).count('1')] = [
                    bin(minterm)[2:].zfill(size)]
        return groups

    def __print_group(self, groups):
        """
        In ra bang gia tri
        """
        print("\n\n\n\nGroup No.\tMinterms\tBinary of Minterms\n%s" %
              ('=' * 50))
        for i in sorted(groups.keys()):
            print("%5d:" % i)  # Prints group number
            for j in groups[i]:
                # Prints minterms and its binary representation
                print("\t\t%-24s%s" %
                      (','.join(self.__find_minterms(j)), j))
            print('-' * 50)

    def __replace(self, tmp, groups, m, marked, should_stop):
        l = sorted(list(tmp.keys()))
        for i in range(len(l) - 1):
            for j in tmp[l[i]]:  # Loop which iterates through current group elements
                for k in tmp[l[i + 1]]:  # Loop which iterates through next group elements
                    res = self.__compare(j, k)  # Compare the minterms
                    if res[0]:  # If the minterms differ by 1 bit only
                        try:
                            # Put a '-' in the changing bit and add it to corresponding group
                            groups[m].append(j[:res[1]] + '-' + j[res[1] + 1:]) if j[:res[1]
                                                                                     ] + '-' + j[res[1] + 1:] not in groups[m] else None
                        except KeyError:
                            # If the group doesn't exist, create the group at first and then put a '-' in the changing bit and add it to the newly created group
                            groups[m] = [j[:res[1]] + '-' + j[res[1] + 1:]]
                        should_stop = False
                        marked.add(j)  # Mark element j
                        marked.add(k)  # Mark element k
            m += 1
        return groups, m, marked, should_stop

    def main(self):
        """
        Toi uu hoa dung Quine
        """
        self.__minterms.sort()
        self.__minterms_with_dont_care.sort()
        size = len(bin(self.__minterms_with_dont_care[-1])) - 2
        all_pi = set()

        # Primary grouping starts
        groups = self.__group_primary(self.__minterms_with_dont_care, size)
        # Primary grouping ends

        # Primary group printing starts
        self.__print_group(groups)
        # Primary group printing ends

        # Process for creating tables and finding prime implicants starts
        while True:
            tmp = groups.copy()
            groups, m, marked, should_stop = {}, 0, set(), True
            groups, m, marked, should_stop = self.__replace(
                tmp, groups, m, marked, should_stop)

            local_unmarked = set(self.__flatten(tmp)).difference(
                marked)  # Unmarked elements of each table
            # Adding Prime Implicants to global list
            all_pi = all_pi.union(local_unmarked)
            print("Unmarked elements(Prime Implicants) of this table:", None if len(local_unmarked)
                  == 0 else ', '.join(
                local_unmarked))  # Printing Prime Implicants of current table
            if should_stop:  # If the minterms cannot be combined further
                print("\n\nAll Prime Implicants: ", None if len(all_pi) ==
                      0 else ', '.join(all_pi))  # Print all prime implicants
                break
            # Printing of all the next groups starts
            self.__print_group(groups)
            # Printing of all the next groups ends
        # Process for creating tables and finding prime implicants ends

        # Printing and processing of Prime Implicant chart starts
        sz = len(str(mt[-1]))  # The number of digits of the largest minterm
        chart = {}
        print('\n\n\nPrime Implicants chart:\n\n    Minterms    |%s\n%s' % (
            ' '.join((' ' * (sz - len(str(i)))) + str(i) for i in mt), '=' * (len(mt) * (sz + 1) + 16)))
        for i in all_pi:
            merged_minterms, y = self.__find_minterms(i), 0
            print("%-16s|" % ','.join(merged_minterms), end='')
            for j in self.__refine(merged_minterms, dc):
                # The position where we should put 'X'
                x = mt.index(int(j)) * (sz + 1)
                print(' ' * abs(x - y) + ' ' * (sz - 1) + 'X', end='')
                y = x + sz
                try:
                    # Add minterm in chart
                    chart[j].append(i) if i not in chart[j] else None
                except KeyError:
                    chart[j] = [i]
            print('\n' + '-' * (len(mt) * (sz + 1) + 16))
        # Printing and processing of Prime Implicant chart ends

        EPI = self.__findEPI(chart)  # Finding essential prime implicants
        print("\nEssential Prime Implicants: " +
              ', '.join(str(i) for i in EPI))
        # Remove EPI related columns from chart
        self.__remove_terms(chart, EPI)

        if len(chart) == 0:  # If no minterms remain after removing EPI related columns
            final_result = [self.__find_variables(i)
                            for i in EPI]  # Final result with only EPIs
        else:  # Else follow Petrick's method for further simplification
            P = [[self.__find_variables(j) for j in chart[i]] for i in chart]
            while len(P) > 1:  # Keep multiplying until we get the SOP form of P
                P[1] = self.__multiply(P[0], P[1])
                P.pop(0)
            # Choosing the term with minimum variables from P
            final_result = [min(P[0], key=len)]
            final_result.extend(self.__find_variables(i)
                                for i in EPI)  # Adding the EPIs to final solution
        print('\n\nSolution: F = ' + ' + '.join(''.join(i)
                                                for i in final_result))


if __name__ == "__main__":
    while True:
        mt = [int(i) for i in input("Enter the minterms: ").strip().split()]
        dc = [int(i) for i in input("Enter the don't cares: ").strip().split()]
        Quine(mt, dc).main()
        check = input("Do you want to quit? (Y/N) ")
        if check == 'Y' or check == 'y':
            break

    input("\nPress enter to exit...")
