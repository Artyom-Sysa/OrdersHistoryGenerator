from Reporter.Reporter import Reporter
from Service.LoggerService.Implementation.DefaultPythonLoggingService import DefaultPythonLoggingService as Logger


class ConsoleReporter(Reporter):
    @staticmethod
    def report(data):
        Logger.info(__file__, 'Start reporting')

        print()
        print('========== REPORT ==========')

        for key in data:
            item = data[key]

            if len(item) > 1:
                max_value = max(item)
                min_value = min(item)
                avg_value = sum(item) / len(item)
                total = sum(item)

                print(key)
                print(f'Max: {max_value} ms')
                print(f'Min: {min_value} ms')
                print(f'Avg: {avg_value} ms')
                print(f'Total: {total} ms')
            else:
                print(f'{key}: {item[0]} ms')
            print('---------------')
            print()

        print('========== REPORT END ==========')
        print()

        Logger.info(__file__, 'Reporting finished')
