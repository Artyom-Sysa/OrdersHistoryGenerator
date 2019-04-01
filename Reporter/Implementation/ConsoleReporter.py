from Reporter.Reporter import Reporter


class ConsoleReporter(Reporter):
    @staticmethod
    def report(data):
        print()
        print('========== REPORT ==========')

        for key in data:
            item = data[key]

            if len(item) > 1:
                max_value = max(item)
                min_value = min(item)
                avg_value = sum(item) / len(item)

                print(key)
                print(f'Max: {max_value} ms')
                print(f'Min: {min_value} ms')
                print(f'Avg: {avg_value} ms')
            else:
                print(f'{key}: {item[0]} ms')
            print('---------------')
            print()

        print('========== REPORT END ==========')
