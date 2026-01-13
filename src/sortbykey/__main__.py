import asyncio
from sortbykey import cli
from sortbykey import workmanager

def main():
    args = cli.parse_args()
    input_dir = args.input
    output_dir = args.output
    num_workers = args.jobs
    asyncio.run(workmanager.start_work(input_dir, output_dir, num_workers))

if __name__ == "__main__":
    main()