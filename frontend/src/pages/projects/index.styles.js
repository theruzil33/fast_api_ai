import styled from 'styled-components'

export const Container = styled.div`
  padding: 2rem;
`

export const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
`

export const Thead = styled.thead`
  background: #f0f0f0;
  text-align: left;
`

export const Th = styled.th`
  padding: 10px 14px;
  border-bottom: 2px solid #ccc;
`

export const Tr = styled.tr`
  border-bottom: 1px solid #eee;
`

export const Td = styled.td`
  padding: 10px 14px;
`

export const EmptyTd = styled(Td)`
  text-align: center;
  color: #888;
`

export const ErrorText = styled.p`
  color: red;
`

export const Toolbar = styled.div`
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
`

export const ActionsRow = styled.div`
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 2rem;
`

export const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
  padding: 1.5rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: #fafafa;
`

export const FormField = styled.div`
  display: flex;
  flex-direction: column;
  gap: 4px;
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

export const Textarea = styled.textarea`
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  resize: vertical;
  min-height: 72px;

  &:focus {
    outline: none;
    border-color: #646cff;
  }
`

export const SubmitButton = styled.button`
  align-self: flex-start;
  padding: 8px 20px;
  background: #646cff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;

  &:hover {
    background: #535bf2;
  }
`

export const FilterRow = styled.div`
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  margin-bottom: 1rem;
`

export const FilterField = styled.div`
  display: flex;
  flex-direction: column;
  gap: 4px;
`

export const Select = styled.select`
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  background: white;
  cursor: pointer;

  &:focus {
    outline: none;
    border-color: #646cff;
  }
`

export const DeleteButton = styled.button`
  padding: 8px 16px;
  background: #e53e3e;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;

  &:disabled {
    background: #ccc;
    cursor: not-allowed;
  }

  &:not(:disabled):hover {
    background: #c53030;
  }
`
