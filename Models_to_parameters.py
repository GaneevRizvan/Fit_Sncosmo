list_nugent = ['nugent-sn1a', 'nugent-sn91t', 'nugent-sn91bg', 'nugent-sn1bc', 'nugent-hyper', 'nugent-sn2n', 'nugent-sn2p','nugent-sn2l']
models_to_parameters = dict([(i, ['z', 't0', 'amplitude']) for i in list_nugent])
models_to_parameters.update([('salt2', ['z', 't0', 'x0', 'x1', 'c'])])