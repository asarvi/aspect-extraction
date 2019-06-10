from model.data_utils import CoNLLDataset
from model.aspect_model import ASPECTModel
from model.config import Config


def align_data(data):

    spacings = [max([len(seq[i]) for seq in data.values()])
                for i in range(len(data[list(data.keys())[0]]))]
    data_aligned = dict()

    # for each entry, create aligned string
    for key, seq in data.items():
        str_aligned = ""
        for token, spacing in zip(seq, spacings):
            str_aligned += token + " " * (spacing - len(token) + 1)

        data_aligned[key] = str_aligned

    return data_aligned



def interactive_shell(model , sentence):



        words_raw = sentence.strip().split(" ")

        preds = model.predict(words_raw)
        to_print = align_data({"input": words_raw, "output": preds})


        aspects = aspectsToarray(words_raw ,preds )
        return aspects

#change B-A type to strings...
def aspectsToarray(sentence,preds):
    aspects = []

    for i in range(len(preds)-2):
        if(preds[i] == 'B-A' and preds[i+1] =='I-A' and preds[i+2] != 'I-A'):

            aspects.append(sentence[i] +" "+sentence[i+1])
        elif(preds[i] == 'B-A' and preds[i+1] =='I-A' and preds[i+2] == 'I-A'):

            aspects.append(sentence[i])
        elif( preds[i] =='B-A' and preds[i+1] =='0'):
            aspects.append(sentence[i])
    if(preds[len(preds)-1] =='B-A'):
        aspects.append(sentence[len(preds)-1])
    if (preds[len(preds) - 2] == 'B-A'):
        aspects.append(sentence[len(preds) - 2])
    #print(aspects)
    return  aspects





def aspectExtractor(sentence):
    # create instance of config
    config = Config()

    # build model
    model = ASPECTModel(config)
    model.build()
    model.restore_session(config.dir_model)

    # create dataset
    test  = CoNLLDataset(config.filename_test, config.processing_word,
                         config.processing_tag, config.max_iter)

    # evaluate and interact
    model.evaluate(test)
    preds=interactive_shell(model , sentence)
    return preds


if __name__ == "__main__":
 print(aspectExtractor("that often feels like a bar of soap just waiting to leap from my hands"))