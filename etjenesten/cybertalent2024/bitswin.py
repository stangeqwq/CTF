bits_string = "0100010001010100101001010100010101010101010101010010101010101000100101010000010010101000100010101001010101000101010101001010001001010010100100101010001010101010100001010100101010101010100010101001010001000010101001000101001010101010010010100010101000010100101010010010101100100101010010100010100101001010100101010101000101001010101010010100100010101010100101001010010010010101001000100100010010100101010000010101000100101000101001010010001000010101001000010010001010010100101001010101001001010101000010001010001010100101010100101001010010010101010010101010010101010100101010101010100101010010000101010101010010101010000101010010101010101001010101001010100010010010010001001000100010101010101001001010101000100010100001010010001001010000100101001000001010100101001001010101010100100101010101000101000010100101010101010100100101001001010101000100010101010101001010010010100001010010010010001000101010010010100100100100101010010010100100010001001001010010101010010100010100100101010101010001000100010000101001010101010010010101"
bits_list = [b for b in bits_string]
heap_count = 0
heap_counts = []
index = 0

# hentet fra database of tallrekker
with open('sprague_grundy_gameofwin.txt', 'r') as f:
    lines = f.readlines()

grundy_values = [int(line.split()[1]) for line in lines]


def grundy_sum(grundy_numbers):
    grundy_sum = 0
    for grundy_number in grundy_numbers:
        grundy_sum ^= grundy_number
    return grundy_sum

# provde a finne tallrekken ved en rekursiv algoritme som beregner
# sprague-grundy tallene (tallene i rettet graf) (litt grafteori og kombinatorisk spillteori)
# omgjøre spillet til et nim-spill med flere "heaps"
def calculate_grundy_number(position):
    not_finished = False
    if position == "1":
        return 0
    elif position == "11":
        return 1
    elif position[-1] == "1" and position[0] == "1": # check for cases such as 100001 and alternating 1010101
        alternating = True
        for i in range(1, len(position)-1):
            if position[i] == "1": not_finished = True
        for i in range(len(position)-1):
            if position[i] == "1" and position[i+1] == "1": alternating = False
        if not not_finished or alternating: 
            return 0
    
    next_positions = [] # used for N(position)
    length = len(position)

    # Generate all possible next positions that is N(position) 
    # to get the set {y: y in N(position)}

    for i in range(0, length - 1):
        next_position = list(position)
        if next_position[i] == "0":
            continue
        if next_position[i] == "1" and next_position[i+1] == "1":
            next_position[i] = "0"
            next_positions.append(''.join(next_position).lstrip("0"))
        
        #print(next_position)
    #print(next_positions)
    # Calculate Grundy numbers of next positions
    next_grundy_numbers = [calculate_grundy_number(pos) for pos in next_positions]
    #print(next_grundy_numbers)

    # Calculate the Grundy number of the current position as the mex of next positions
    grundy_number = mex(next_grundy_numbers)
    #print(f"grundy number of {position}: {grundy_number}")

    return grundy_number

def mex(grundy_numbers_list):
    grundy_numbers_list = list(set(sorted(grundy_numbers_list)))
    if grundy_numbers_list[0] != 0:
        return 0
    mex_value = 1
    for i in range(len(grundy_numbers_list) - 1):
        if grundy_numbers_list[i] + 1 == grundy_numbers_list[i+1]:
            mex_value += 1
        else: break
    return mex_value

def heap_check_for_splits(bits_string): # we check if the current heap is being split
    for index in range(2, len(bits_string) - 3):
        if bits_string[index] == "0" and bits_string[index+1] == "1" and bits_string[index+2] == "1":
            return True
        if bits_string[index] == "0" and bits_string[index-1] == "1" and bits_string[index-2] == "1": 
            return True

def calculate_heap_counts(bits_string):
    count = 0
    counts = []
    for b in bits_string:
        if b == "1": 
            count += 1
        else:
            if count > 1:
                counts.append(count)
            count = 0
    if count > 1:
        counts.append(count)
    return counts

counts = calculate_heap_counts(bits_string)
print(counts)
print(len(grundy_values))

def make_move(bits_string):
    possible_moves = []
    for i in range(len(bits_string)-1):
        if bits_string[i] == "1" and bits_string[i+1] == "1":
            bits_string_list = [b for b in bits_string]
            bits_string_list[i] = "0"
            possible_moves.append(''.join(bits_string_list))
            possible_moves.append(i)
    for i in range(0, len(possible_moves), 2):
        counts = calculate_heap_counts(possible_moves[i])
        g_values = []
        for count in counts:
            g_values.append(grundy_values[count]) 
        print(f"Move {possible_moves[i+1]}: {grundy_sum(g_values)}")
        #print(g_values)
    



'''NUMBER FOUND ARE THE SAME VALUES AS COUPLES-ARE-FOREVER
for length in range(2, 16):
    initial_position = "1" * length
    result = calculate_grundy_number(initial_position)
    print(f"The Grundy number of {initial_position} is: {result}")
'''
g_values = []
for count in counts:
    g_values.append(grundy_values[count])

print(g_values)
print(grundy_sum(g_values))
make_move(bits_string)
