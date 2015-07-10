import optparse
import sys

from sklearn.cross_validation import train_test_split


def main():
    parser = optparse.OptionParser()

    parser.add_option('--module', action='store')
    parser.add_option('--training', action='store')
    options, args = parser.parse_args()
    if not options.module:
        print 'Usage: python model_test_harness.py --module path/to/model.py'
        return
    module_name = options.module.replace('.py', '').replace('/', '.')
    training_filename = options.training or \
            options.module[:options.module.rfind('/')] + '/train.csv'

    try:
        module_package = __import__(module_name)
    except:
        msg = 'Unable to import "%(m)s". Investigate with interpreter, '
        msg = msg + 'running "__import__(%(m)s)" to investigate'
        raise Exception(msg  % {'m': module_name})

    model_module = getattr(module_package, module_name.split('.')[-1])
    model = model_module.build_model()
    Xs, y = model.load_training(training_filename)
    X_train, X_test, y_train, y_test = train_test_split(Xs, y, test_size=0.25)
    y_hat = model.model_and_predict(X_train, y_train, X_test)

    print sum(y_hat == y_test) / float(len(y_hat))


if __name__ == '__main__':
    main()