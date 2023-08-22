import sys

def format_csv_lines(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file:
        lines = input_file.readlines()

    formatted_lines = [','.join(line.replace(' ', '').split(',')) for line in lines if ',' in line]
    output_text = ''.join(formatted_lines)

    with open(output_file_path, 'w') as output_file:
        output_file.write(output_text)

    print("Output has been written to", output_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file output_file")
    else:
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        format_csv_lines(input_file_path, output_file_path)
