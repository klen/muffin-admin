import { useDataProvider } from "react-admin"
import { useMutation } from "react-query"

export default function useAction(resource, action) {
  const dataProvider = useDataProvider()
  return useMutation((params) =>
    dataProvider.runAction(resource, action, params)
  )
}
