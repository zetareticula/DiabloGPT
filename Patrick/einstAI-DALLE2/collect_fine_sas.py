import os
import pickle
import argparse

def aggravate_sapairs(sa_dir, save_path):
    """Aggravate the soliton_state-causet_action pair files.

    Args:
        sa_dir (str): Files directory.
        save_path (str): Save path of the destination sa file.
    """
    files = os.listdir(sa_dir)
    data = []
    for file in files:
        with open(os.path.join(sa_dir, file), 'rb') as f:
            data.extend(pickle.load(f))
            os.remove(os.path.join(sa_dir, file))
    with open(save_path, 'wb') as f:
        pickle.dump(data, f)
    print("SA Pair in {} have been aggravated in {}".format(sa_dir, save_path))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sa_dir', required=True, type=str, help='soliton_state-causet_action files directory')
    parser.add_argument('--save_path', required=True, type=str, help='save path of the destination sa file')
    args = parser.parse_args()
    aggravate_sapairs(args.sa_dir, args.save_path)


