from const import TARGET_DATA
import shutil, os

def analyze_repo(path, output_path, repo_url, commit_hash):
    from git import Repo

    repo = Repo.clone_from(repo_url, path, no_checkout=True)
    repo.git.checkout(commit_hash)

    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    os.makedirs(output_path)

    instruction = 'java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar {}'.format(path)
    os.system(instruction)

    for f in os.listdir('./'):
        if f.endswith('.csv'):
            shutil.move(f, output_path)

if __name__ == '__main__':
    repo_url = TARGET_DATA['repo_url']
    for val in TARGET_DATA['commits_and_semesters']:
        semester = val['semester']
        commit_hash = val['hash_commit']
        output_path = '../data/{}'.format(semester)
        clone_path = semester

        try:
            analyze_repo(clone_path, output_path, repo_url, commit_hash)
        except BaseException as e:
            print('Error!')
            print(str(e))
            if os.path.exists(output_path):
                shutil.rmtree(output_path)
        else:
            print('Success for {}!'.format(semester))
        finally:
            if os.path.exists(clone_path):
                shutil.rmtree(clone_path)
