from push_sum import PushSum


def test_init():
    ps = PushSum(3)
    assert len(ps.group.group_members) == 2
