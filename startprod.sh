#/bin/bash
export FLASK_APP=pegasus
export FLASK_ENV=development
python -m flask run --host=0.0.0.0 --port=$port