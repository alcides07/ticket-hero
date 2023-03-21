import styled from "styled-components";

export const ContainerHeader = styled.nav`
    display: flex;
    justify-content:center;
    background-color: #FCFCFC;
    height: 10vh;
    width: 100%;
    
    ul{
        display: flex;
        align-items: center;
        list-style: none;
        margin: 0;
        padding: 0;
    }
    
    li{
        font-weight: 400;
        font-size: 1.1em;
        margin: 5vw; 
        transition: 0.5s;
    }

    li:hover {
        color: #FF914D;
        cursor: pointer;
    }
`;