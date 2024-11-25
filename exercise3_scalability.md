# Exercise 3: Scaling the Loss Calculation Model

## Scalability Analysis:

The current script works fine for small datasets but would struggle with larger ones because it loads the entire file into memory, which can quickly lead to I/O bottlenecks on most machines. Also, the calculations for each building could cause CPU slowdowns, especially when iterating over the building_data list for large datasets.

## Optimization Strategies:

The first option that comes to mind is using NumPy. It’s a widely used library in data science and mathematics in general. Working with NumPy vectors can simplify computations and make things more extendable. Additionally, NumPy arrays use less memory and storage compared to Python’s lists. However, even with NumPy the main issue still persists: we’d be reading the entire file into memory at once.

To address this we could use NumPy’s memmap package. This package allows you to read and write chunks of data without loading the entire array into memory. The downside is that this requires converting the input file to a binary format. Because of this, I wouldn’t recommend this approach as the first option, assuming we want to keep the file format as it is.

Instead, my first choice would be to use ijson with generators. ijson is designed to read large JSON files object by object, without loading the entire file into memory. Generators also help by computing values only when needed, instead of storing everything in memory at once.

The following snippet shows how to process the file in a memory-efficient manner using the mentioned approached.

```
import ijson

def load_json_object_by_object(file_path):
    with open(file_path, 'r') as f:
        objects = ijson.items(f, 'item')

        for obj in objects:
            yield obj

def calculate_projected_losses(file_path, number_of_years=1):
    total_loss = 0

    for building in load_json_object_by_object(file_path):
        # ...
        # total_loss += present_value_loss

    return total_loss


def main():
    file_path = 'data.json'
    total_projected_loss = calculate_projected_losses(file_path)
    print(f"Total Projected Loss: ${total_projected_loss:.2f}")


if __name__ == '__main__':
    main()

```

The previous approach should work in most cases, but if the calculations become too complex, CPU bottlenecks might occur. In that case, I’d try parallel processing using multiprocessing.Pool, since the task is both I/O-bound and CPU-bound. However, this introduces a new challenge: the file needs to be split into several chunks. To handle this, we can use a separate thread to split the file before processing it in parallel.

## Resource Management:

The first factor that impacts memory and CPU usage is the size of the data. From there, we need to consider whether the data can be split and if the current format is optimal.

If the calculations are inefficient or more complex than necessary, CPU bottlenecks can happen. Identifying and extracting common elements that don't change, and considering caching where applicable, can help mitigate this.

If we choose to split the workload across different processes or threads, it's importat to consider how the data is split and how the results are aggregated. Using queues for buffering can also help, as well as ensuring that work is distributed evenly across processes.
