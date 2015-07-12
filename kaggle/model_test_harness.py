import optparse

from sklearn.cross_validation import train_test_split


def evaluate_model(model, X_train, y_train, X_test, y_test):
    y_hat = model.model_and_predict(X_train, y_train, X_test)
    print model.__class__, sum(y_hat == y_test) / float(len(y_hat))


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

    delegator = getattr(module_package, module_name.split('.')[-1])
    models = delegator.models()
    data_model = delegator.KaggleDataModel()
    Xs, y = data_model.load_training(training_filename)
    X_train, X_test, y_train, y_test = train_test_split(Xs, y, test_size=0.25)
    
    for model in models:
        evaluate_model(model, X_train, y_train, X_test, y_test)


if __name__ == '__main__':
    main()