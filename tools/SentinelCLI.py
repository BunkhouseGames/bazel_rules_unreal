import click

@click.command()
@click.option('--dummy_argument')

def RefreshContentBuildFiles(dummy_argument):
    """Injects Asset Validation tests for UE content"""

    print("Hello world")
    print(dummy_argument)

if __name__ == '__main__':
    RefreshContentBuildFiles()