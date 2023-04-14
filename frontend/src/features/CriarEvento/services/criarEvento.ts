import { IEvento } from './../../../types/IEvento';
import {api, headers} from "../../../services/api";
import {notify} from "../../../components/Toastify";
import { IToast } from "../../../types/IToast";

export const criarEvento = (dadosEvento:IEvento) => {
    return api.post("/evento/", 
    {
        nome:dadosEvento["nome"], 
        categoria:dadosEvento["categoria"],
        descricao:dadosEvento["descricao"],
        valorIngresso:dadosEvento["valorIngresso"],
        ingressoTotal:dadosEvento["ingressoTotal"],
        data:dadosEvento["data"],
        local: dadosEvento["local"],
        publico: dadosEvento["publico"],
        idadeMinima: dadosEvento["idadeMinima"],
        pathImg: dadosEvento["pathImg"]
    }, 
    {headers: headers})
    .then((response) => {
        const toast: IToast = {
            message: "Evento criado com sucesso!",
            variant: 'success',
        }; 
        notify(toast);
        return response.data;
    })
    .catch((error) => {
        console.log('erro', error);
    });
};