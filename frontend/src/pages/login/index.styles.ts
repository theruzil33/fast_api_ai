import styled from 'styled-components'

export const PageWrapper = styled.div`
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
`

export const Card = styled.div`
  background: white;
  padding: 2.5rem 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 360px;
`

export const Title = styled.h1`
  margin: 0 0 1.5rem;
  font-size: 1.5rem;
  text-align: center;
  color: #222;
`

export const Field = styled.div`
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 1rem;
`

export const Label = styled.label`
  font-size: 0.875rem;
  font-weight: 600;
  color: #444;
`

export const Input = styled.input`
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;

  &:focus {
    outline: none;
    border-color: #646cff;
  }
`

export const SubmitButton = styled.button`
  width: 100%;
  padding: 10px;
  margin-top: 0.5rem;
  background: #646cff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;

  &:hover {
    background: #535bf2;
  }

  &:disabled {
    background: #aaa;
    cursor: not-allowed;
  }
`

export const ErrorText = styled.p`
  color: red;
  font-size: 0.875rem;
  margin: 0.5rem 0 0;
`
