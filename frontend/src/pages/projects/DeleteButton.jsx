import { Toolbar, DeleteButton as StyledDeleteButton } from './index.styles'

function DeleteButton({ count, onDelete }) {
  return (
    <Toolbar>
      <StyledDeleteButton onClick={onDelete} disabled={count === 0}>
        Delete{count > 0 ? ` (${count})` : ''}
      </StyledDeleteButton>
    </Toolbar>
  )
}

export default DeleteButton
