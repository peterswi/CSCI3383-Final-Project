import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math


def swap(inpArray, i, j):
    """Helper function to swap elements i and j of list inpArray."""

    if i != j:
        inpArray[i], inpArray[j] = inpArray[j], inpArray[i]

def bubblesort(inpArray):
    """In-place bubble sort."""

    if len(inpArray) == 1:
        return

    swapped = True
    for i in range(len(inpArray) - 1):
        if not swapped:
            break
        swapped = False
        for j in range(len(inpArray) - 1 - i):
            if inpArray[j] > inpArray[j + 1]:
                swap(inpArray, j, j + 1)
                swapped = True
            yield inpArray

def insertionsort(inpArray):
    """In-place insertion sort."""

    for i in range(1, len(inpArray)):
        j = i
        while j > 0 and inpArray[j] < inpArray[j - 1]:
            swap(inpArray, j, j - 1)
            j -= 1
            yield inpArray

#Jerry's new insertion sort, used in bucket sort. 
def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >=0 and key < arr[j] :
                arr[j+1] = arr[j]
                j -= 1
                yield arr
        arr[j+1] = key
    yield arr
    
#yields arent right but we are getting there
def bucketSort(inpArray, bucket_num=10):
    maxValue = inpArray[0]
    for i in range(1, len(inpArray)):
        if inpArray[i] > maxValue:
            maxValue = inpArray[i]
    buckets = []
    for i in range(0, bucket_num):
        buckets.append([])
    for i in range(0, len(inpArray)):
        buckets[math.floor((bucket_num * inpArray[i]) /(maxValue+1))].append(inpArray[i])
    arr = []
    for i in range(0, len(buckets)):
        yield from insertionSort(buckets[i])
        for j in range(0, len(buckets[i])):
            arr.append(buckets[i][j])
            yield arr
    yield arr

def mergesort(inpArray, start, end):
    """Merge sort."""

    if end <= start:
        return

    mid = start + ((end - start + 1) // 2) - 1
    yield from mergesort(inpArray, start, mid)
    yield from mergesort(inpArray, mid + 1, end)
    yield from merge(inpArray, start, mid, end)
    yield inpArray

def merge(inpArray, start, mid, end):
    """Helper function for merge sort."""

    merged = []
    leftIdx = start
    rightIdx = mid + 1

    while leftIdx <= mid and rightIdx <= end:
        if inpArray[leftIdx] < inpArray[rightIdx]:
            merged.append(inpArray[leftIdx])
            leftIdx += 1
        else:
            merged.append(inpArray[rightIdx])
            rightIdx += 1

    while leftIdx <= mid:
        merged.append(inpArray[leftIdx])
        leftIdx += 1

    while rightIdx <= end:
        merged.append(inpArray[rightIdx])
        rightIdx += 1

    for i, sorted_val in enumerate(merged):
        inpArray[start + i] = sorted_val
        yield inpArray

def quicksort(inpArray, start, end):
    """In-place quicksort."""

    if start >= end:
        return

    pivot = inpArray[end]
    pivotIdx = start

    for i in range(start, end):
        if inpArray[i] < pivot:
            swap(inpArray, i, pivotIdx)
            pivotIdx += 1
        yield inpArray
    swap(inpArray, end, pivotIdx)
    yield inpArray

    yield from quicksort(inpArray, start, pivotIdx - 1)
    yield from quicksort(inpArray, pivotIdx + 1, end)


#The way we have written it, we have to build a maxHeap and then we place largest at then
    #end of the array and keep popping the largest until it is sorted from front to back
    #in ascending order
def heapify(inpArray, n, i):
    largest = i # Initialize smallest as root
    l = 2 * i + 1     # left = 2*i + 1
    r = 2 * i + 2     # right = 2*i + 2

    # See if left child of root exists and is
    #lesser than root
    if l < n and inpArray[largest] < inpArray[l]:
        largest = l

    # See if right child of root exists and is
    # lesser than root
    if r < n and inpArray[largest] < inpArray[r]:
        largest = r

    # Change root, if needed
    if largest != i:
        swap(inpArray, i, largest)
        # Heapify the root.
        yield from heapify(inpArray, n, largest)
    yield inpArray


# The main function to sort an array of given size
def heapSort(inpArray):
    n = len(inpArray)
    # Build a maxheap.
    for i in range(n, -1, -1):
        yield from heapify(inpArray, n, i)

    # One by one extract elements
    for i in range(n-1, 0, -1):
        #i think we need a couple more yields in here but at least it is working correctly
        swap(inpArray, i, 0)
        yield from heapify(inpArray, i, 0)
        yield inpArray

#Jerry's Radix Sort
def radixSort(inpArray):
    arr = inpArray[:]
    bucketCount = 10
    #find largest number
    largest = max(arr)
    #digit count in largest num
    maxDigit = len(str(largest))
    for digit in range(1, maxDigit+1):
    	#new bucket each time
    	buckets = [[] for x in range(bucketCount)]
    	#digits to places
    	division = 10**(digit-1)
    	#append to bucket
    	for x in arr:
    		currDigit = int((x//division)%bucketCount)
    		buckets[currDigit].append(x)
		#remove elements from bucket
    	i = 0
    	for bucket in buckets:
    		for x in bucket:
    			arr[i] = x
    			i = i + 1
    			yield arr
    yield arr


def selectionsort(inpArray):
    """In-place selection sort."""
    if len(inpArray) == 1:
        return

    for i in range(len(inpArray)):
        # Find minimum unsorted value.
        minVal = inpArray[i]
        minIdx = i
        for j in range(i, len(inpArray)):
            if inpArray[j] < minVal:
                minVal = inpArray[j]
                minIdx = j
            yield inpArray
        swap(inpArray, i, minIdx)
        yield inpArray

if __name__ == "__main__":
    # Get user input to determine range of integers (1 to inpLen) and desired
    # sorting method (algorithm). Else integers are randomly generated.

    inputArr=[]
    generation = input("Select Integer Input Method:\nm for manual\nr for random\n")
    inpLen = int(input("Enter Number of Integers to be Sorted:"))
    if generation == "m":
        print("Enter the " + str(inpLen) + " integers to be sorted: ")
        for i in range(inpLen):
            element = int(input())
            inputArr.append(element)
    elif generation == "r":
        for i in range(inpLen):
            element = random.randint(0, 200)
            inputArr.append(element)
    random.shuffle(inputArr)
    displayArr = inputArr #to display the original shuffled array 
    print("Shuffled array to be sorted = ", inputArr, "\n")
    speed = input("Enter sort speed (default medium):\ns for slow\nf for fast\n")
    method = input("""Enter sorting method:\nbb for bubble\ni for insertion\nm for merge\nq for quick\nh for heap\nr for radix \nbu for bucket \ns for selection (default)\n""")
    
    delay=250
    if speed =="s":
        delay= 400
    elif speed=="f":
        delay=100

    

    # Get appropriate generator to supply to matplotlib FuncAnimation method.
    if method == "bb":
        title = "Bubble sort"
        generator = bubblesort(inputArr)
    elif method == "i":
        title = "Insertion sort"
        generator = insertionsort(inputArr)
    elif method == "m":
        title = "Merge sort"
        generator = mergesort(inputArr, 0, inpLen - 1)
    elif method == "q":
        title = "Quicksort"
        generator = quicksort(inputArr, 0, inpLen - 1)
    elif method == "h":
        title = "Heap Sort"
        generator = heapSort(inputArr)
    elif method == 'r':
        title = "Radix Sort"
        generator = radixSort(inputArr)
    elif method == 'bu':
        title = "Bucket Sort"
        num_buckets = 10
        generator = bucketSort(inputArr, num_buckets)
    else: #selection sort acts as the default when s or any incorrect input is entered
        title = "Selection sort"
        generator = selectionsort(inputArr)

    # Initialize figure and axis.
    fig, ax = plt.subplots()
    ax.set_title(title)

    #init the bars to be placed in the bar chart display
    bar_rects = ax.bar(range(len(inputArr)), inputArr, align="edge", color="whitesmoke",
                       edgecolor="darkgreen")

    #setting the dimensions of the graph
    ax.set_xlim(0, inpLen)
    ax.set_ylim(0, max(inputArr)+int(0.15*max(inputArr))+1)

    #setting a text box for the number of operations
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)
    text2 = ax.text(0.02, 0.85, "", transform=ax.transAxes, wrap=True)
	
    # update_fig utilizes FuncAnimation() to track # of operations (number of times
    # we are yielding an array + number of comparisons).
	
    iteration = [0]
    def update_fig(inpArray, rects, iteration):
        for rect, val in zip(rects, inpArray):
            rect.set_height(val)
            #would be interesting to try and tinker with a color variable that is global to follow the changed rect
      #      rect.set_color(
        iteration[0] += 1
        text.set_text("# of operations: {}".format(iteration[0]))
        text2.set_text("Array = {}".format(inpArray))
     #   rects[iteration[0]].set_color('r')

    anim = animation.FuncAnimation(fig, func=update_fig,
        fargs=(bar_rects, iteration), frames=generator, interval=delay,
        repeat=False)
    plt.show()
